from django.shortcuts import render
from rest_framework import viewsets

from .models import Asset, Interface
from .serializers import AssetSerializer, InterfaceSerializer


class AssetViewSet(viewsets.ModelViewSet):
    serializer_class = AssetSerializer
    queryset = Asset.objects

class InterfaceViewSet(viewsets.ModelViewSet):
    serializer_class = InterfaceSerializer
    queryset = Interface.objects

