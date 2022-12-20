from django.urls import path
from .views import (
    UploadMediaAPIView
)

urlpatterns = [
    path('upload-media/', UploadMediaAPIView.as_view(),
         name='upload-media'),

]
