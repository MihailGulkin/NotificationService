from rest_framework import generics

from .serializers import ClientSerializer
from .models import Client


class ClientListAPIView(generics.ListAPIView):
    """
    Display a list :model:`client.Client`.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientCreateAPIView(generics.CreateAPIView):
    """
    Create :model:`client.Client`.
    """
    serializer_class = ClientSerializer


class ClientDestroyAPIView(generics.DestroyAPIView):
    """
    Destroy :model:`client.Client`.
    """
    lookup_field = 'pk'
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientUpdateAPIView(generics.UpdateAPIView):
    """
    PUT/PATCH :model:`client.Client`.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    lookup_field = 'pk'
