import django_filters.rest_framework
from rest_framework import viewsets

from .models import AssetType, Asset, ISPDNClass, GISClass, ASUTPClass, KIIClass
from .serializers import AssetTypeSerializer, AssetSerializer, ISPDNClassSerializer, GISClassSerializer, \
    ASUTPClassSerializer, KIIClassSerializer


class AssetTypeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AssetTypeSerializer
    queryset = AssetType.objects.all()


class AssetsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AssetSerializer
    queryset = Asset.objects.select_related('asset_type', 'vendor').all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['asset_type',]


class ISPDNClassesViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ISPDNClassSerializer
    queryset = ISPDNClass.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = {'type': ['in'], 'specification': ['in'], 'protection_level': ['exact']}


class GISClassesViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GISClassSerializer
    queryset = GISClass.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = {'size': ['exact'], 'specification': ['in'], 'protection_class': ['exact']}


class ASUTPClassesViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ASUTPClassSerializer
    queryset = ASUTPClass.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = {'specification': ['in'], 'protection_class': ['exact']}


class KIIClassesViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = KIIClassSerializer
    queryset = KIIClass.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = {'specification': ['in'], 'significance_attribute': ['exact']}
