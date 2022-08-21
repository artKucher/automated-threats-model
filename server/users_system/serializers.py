from rest_framework import serializers

from users_system.models import System


class SystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = System
        fields = ['id',
                  'ispdn_classes',
                  'gis_classes',
                  'asutp_classes',
                  'kii_classes',
                  'assets',
                  'negative_consequences',
                  'name']