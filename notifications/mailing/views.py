from rest_framework import generics

from client.tasks import run_client_mailing
from .services import create_periodical_task

from .searilizers import (
    MailingSerializer,
    MessageSerializer
)
from .models import (
    Mailing,
    Message
)


class MessageListAPIView(generics.ListAPIView):
    """
    Display a list :model:`mailing.Message`.
    """
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def get_queryset(self):
        return self.queryset.filter(
            mailing_id_id=self.kwargs['mailing_id']
        )


class MailingListAPIView(generics.ListAPIView):
    """
    Display a list :model:`mailing.Mailing`.
    """
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer


class MailingCreateAPIView(generics.CreateAPIView):
    """
    Create :model:`mailing.Mailing`.
    After create run root client_mailing task
    """
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer

    def perform_create(self, serializer):
        instance = serializer.save()

        run_client_mailing.apply_async(
            args=(instance.pk,),
            eta=instance.start_mailing_time,
        )
        create_periodical_task()


class MailingDestroyAPIView(generics.DestroyAPIView):
    """
    Destroy :model:`mailing.Mailing`.
    """
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer


class MailingUpdateAPIView(generics.UpdateAPIView):
    """
    PUT/PATCH :model:`mailing.Mailing`.
    """
    queryset = Mailing.objects.all()
    serializer_class = MailingSerializer
