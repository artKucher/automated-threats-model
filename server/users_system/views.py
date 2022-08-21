import json
from dataclasses import asdict

import django_filters.rest_framework
from django.http import FileResponse, HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from services.report.builder import ReportBuilder
from services.report.printer import ReportPrinter
from users_system.models import System
from users_system.serializers import SystemSerializer


class SystemViewSet(viewsets.ModelViewSet):
    serializer_class = SystemSerializer
    queryset = System.objects.all()

    @action(detail=True)
    def build_report(self, request, pk=None):
        system = System.objects.get(id=pk)
        report = ReportBuilder(system).build()
        document = ReportPrinter(report).print()
        response =  HttpResponse(
            document.getvalue(),
            content_type='application/vnd.oasis.opendocument.text',
        )
        response['Content-Disposition'] = f'attachment; filename="{system.name}_report.odt"'
        return response