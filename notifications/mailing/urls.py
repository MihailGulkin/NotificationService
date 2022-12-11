from django.urls import path
from .views import (
    MailingCreateAPIView,
    MailingListAPIView,
    MailingUpdateAPIView,
    MailingDestroyAPIView,

    MessageListAPIView,
)

urlpatterns = [
    path('create-mailing/', MailingCreateAPIView.as_view(),
         name='create-mailing'),
    path('list-mailing/', MailingListAPIView.as_view(),
         name='list-mailing'),
    path('update-mailing/<int:pk>/', MailingUpdateAPIView.as_view(),
         name='update-mailing'),
    path('destroy-mailing/<int:pk>/', MailingDestroyAPIView.as_view(),
         name='destroy-mailing'),

    path('list-message/<int:mailing_id>/', MessageListAPIView.as_view(),
         name='list-message-mailing_pk')
]
