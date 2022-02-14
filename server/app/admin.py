from django.contrib import admin

# Register your models here.
from .models import Asset, Interface, Capabilities, Attacker, Vulnerability, Threat

admin.site.register(Asset)
admin.site.register(Interface)
admin.site.register(Capabilities)
admin.site.register(Attacker)
admin.site.register(Vulnerability)
admin.site.register(Threat)