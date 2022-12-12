from django.db import models
from django.core.validators import (
    RegexValidator,
    MinValueValidator,
    MaxValueValidator,
    ValidationError
)

from pytz import all_timezones


class Tag(models.Model):
    """
    Stores a many tag related to :model:`client.Client`.
    """
    tag_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.tag_name}'


class Client(models.Model):
    """
    Store client data, used for send user notification.
    """
    TIMEZONE_SET = zip(all_timezones, all_timezones)
    phone_number = models.CharField(
        unique=True,
        validators=[RegexValidator(regex=r"^7\d{10}$",
                                   message="Incorrect number")],
        max_length=11,

    )
    operator_code = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(900), MaxValueValidator(999)],
    )
    tag = models.ManyToManyField(Tag)
    timezone = models.CharField(
        max_length=32,
        default='Europe/Moscow',
        choices=TIMEZONE_SET
    )

    def clean(self, *args, **kwargs):
        if str(self.operator_code) != self.phone_number[1:4]:
            raise ValidationError('Operator code != Phone number operator')
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Id: {self.pk} - Phone: +{self.phone_number}'
