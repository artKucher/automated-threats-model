import django_filters.rest_framework
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    AssetType,
    Asset,
    ISPDNClass,
    GISClass,
    ASUTPClass,
    KIIClass,
    NegativeConsequence,
)
from .serializers import (
    AssetTypeSerializer,
    AssetSerializer,
    ISPDNClassSerializer,
    GISClassSerializer,
    ASUTPClassSerializer,
    KIIClassSerializer,
    NegativeConsequenceSerializer,
    AssetIdsSerializer,
)


class NegativeConsequenceMixin:
    @action(detail=False)
    def negative_consequences(self, request):
        ids_list = self.filter_queryset(self.queryset.negative_consequences_ids())
        negative_consequences = NegativeConsequence.objects.filter(id__in=ids_list)
        serializer = NegativeConsequenceSerializer(negative_consequences, many=True)
        return Response(
            {
                'count': negative_consequences.count(),
                'results': serializer.data
            }
        )


class AssetTypeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AssetTypeSerializer
    queryset = AssetType.objects.all()


class AssetsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AssetSerializer
    queryset = Asset.objects.select_related('asset_type', 'vendor').all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = {'asset_type': ['in']}


class AssetsIdsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = AssetIdsSerializer
    queryset = Asset.objects.select_related('asset_type').all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = {'asset_type': ['in']}
    pagination_class = None


class ISPDNClassesViewSet(NegativeConsequenceMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = ISPDNClassSerializer
    queryset = ISPDNClass.objects
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = {'type': ['in'], 'specification': ['in'], 'protection_level': ['exact']}


class GISClassesViewSet(NegativeConsequenceMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = GISClassSerializer
    queryset = GISClass.objects
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = {'size': ['exact'], 'specification': ['in'], 'protection_class': ['exact']}


class ASUTPClassesViewSet(NegativeConsequenceMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = ASUTPClassSerializer
    queryset = ASUTPClass.objects
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = {'specification': ['in'], 'protection_class': ['exact']}


class KIIClassesViewSet(NegativeConsequenceMixin, viewsets.ReadOnlyModelViewSet):
    serializer_class = KIIClassSerializer
    queryset = KIIClass.objects
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = {'specification': ['in'], 'significance_attribute': ['exact']}


class NegativeConsequencesViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NegativeConsequenceSerializer
    queryset = NegativeConsequence.objects.select_related('group').all()
    pagination_class = None
