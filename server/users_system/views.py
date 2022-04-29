import django_filters.rest_framework
from rest_framework import viewsets

from users_system.models import System
from users_system.serializers import SystemSerializer


class SystemViewSet(viewsets.ModelViewSet):
    serializer_class = SystemSerializer
    queryset = System.objects.all()
