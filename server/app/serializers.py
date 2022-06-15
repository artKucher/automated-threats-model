from rest_framework import serializers

from app.models import AssetType, Interface, Asset, ISPDNClass, GISClass, ASUTPClass, KIIClass, KIISpecificationChoices, \
    ISPDNSpecificationChoices, NegativeConsequence


class AssetTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetType
        fields = ['id', 'name']


class AssetSerializer(serializers.ModelSerializer):
    asset_type_name = serializers.StringRelatedField(source='asset_type')
    vendor_name = serializers.StringRelatedField(source='vendor')
    class Meta:
        model = Asset
        fields = ['id',
                  'name',
                  'asset_type',
                  'asset_type_name',
                  'vendor',
                  'vendor_name']


class AssetIdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id']


class ISPDNClassSerializer(serializers.ModelSerializer):

    class Meta:
        model = ISPDNClass
        fields = ['id',
                  'type',
                  'specification',
                  'protection_level']


class GISClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = GISClass
        fields = ['id',
                  'size',
                  'specification',
                  'protection_class']


class ASUTPClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = ASUTPClass
        fields = ['id',
                  'specification',
                  'protection_class']


class KIIClassSerializer(serializers.ModelSerializer):
    specification = serializers.ChoiceField(choices=KIISpecificationChoices)
    class Meta:
        model = KIIClass
        fields = ['id',
                  'specification',
                  'significance_attribute']


class NegativeConsequenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NegativeConsequence
        fields = ['id',
                  'description',
                  'full_name']
