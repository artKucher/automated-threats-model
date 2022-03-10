from django.contrib import admin

# Register your models here.
from .models import Asset, AssetType, Vendor, Interface, Attacker, Vulnerability, Threat

admin.site.register(Asset)
admin.site.register(AssetType)
admin.site.register(Vendor)
admin.site.register(Interface)
admin.site.register(Attacker)
admin.site.register(Vulnerability)
admin.site.register(Threat)