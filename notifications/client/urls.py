from django.urls import path
from .views import (
    ClientListAPIView,
    ClientCreateAPIView,
    ClientUpdateAPIView,
    ClientDestroyAPIView
)

urlpatterns = [
    path('all-client/', ClientListAPIView.as_view(),
         name='all-client'),
    path('create-client/', ClientCreateAPIView.as_view(),
         name="create-client"),
    path('destroy-client/<int:pk>/', ClientDestroyAPIView.as_view(),
         name='destroy-client'),
    path('update-client/<int:pk>/', ClientUpdateAPIView.as_view(),
         name='update-client'),
]
