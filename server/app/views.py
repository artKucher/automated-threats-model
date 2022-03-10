from django.shortcuts import render
from rest_framework import viewsets

from .models import AssetType, Interface
from .serializers import AssetSerializer, InterfaceSerializer


class AssetViewSet(viewsets.ModelViewSet):
    serializer_class = AssetSerializer
    queryset = AssetType.objects

class InterfaceViewSet(viewsets.ModelViewSet):
    serializer_class = InterfaceSerializer
    queryset = Interface.objects

