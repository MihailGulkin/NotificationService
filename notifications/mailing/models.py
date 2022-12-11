from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

from client.models import Tag
from http import HTTPStatus


class Filter(models.Model):
    """
    Store a single filter related to :model:`mailing.Mailing`.
    """
    OPERATOR_CODE = "Operator"
    TAG = "Tag"
    CLIENT_FILTER = [
        (OPERATOR_CODE, "Code mobile operator"),
        (TAG, "Tag")
    ]

    filter_type = models.CharField(
        max_length=100,
        choices=CLIENT_FILTER
    )
    filter_value = models.CharField(max_length=100)

    def clean(self, *args, **kwargs):
        if self.filter_type == Filter.OPERATOR_CODE:
            if not self.filter_value.isnumeric():
                raise ValidationError(
                    'Incorrect operator code')
            value = int(self.filter_value)
            if not (900 <= value <= 999):
                raise ValidationError(
                    'Incorrect operator code')
            super().save(*args, **kwargs)
            return
        if not Tag.objects.filter(tag_name=self.filter_value).exists():
            raise ValidationError("Incorrect Tag")
        super().save(*args, **kwargs)


class Mailing(models.Model):
    """
    When created, if start.time < now.time < end.time start celery task
    """
    start_mailing_time = models.DateTimeField()
    message_text = models.CharField(max_length=20_000)
    client_filter = models.ForeignKey(Filter, on_delete=models.CASCADE)
    end_mailing_time = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self, *args, **kwargs):
        if not (self.start_mailing_time and self.end_mailing_time):
            return
        if self.start_mailing_time >= self.end_mailing_time:
            raise ValidationError("Invalid start-end time; Need start < end")
        if self.end_mailing_time < timezone.now():
            raise ValidationError("Date already gone")
        super().save(*args, **kwargs)

    def __str__(self):
        return f'pk: {self.pk}'


class Message(models.Model):
    """
    Store message history, creates a notification after a request
    on external api
    """
    STATUS_CHOICES = [(status.value, status.name) for status in HTTPStatus]

    mailing_send = models.DateTimeField()
    mailing_status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES)
    mailing_id = models.ForeignKey(Mailing, on_delete=models.CASCADE,
                                   related_name='mailing_msg')
    client_id = models.ForeignKey('client.Client', on_delete=models.CASCADE)
