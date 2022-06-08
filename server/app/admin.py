from django.contrib import admin

from .models import (
    Asset,
    AssetType,
    Vendor,
    Interface,
    AttackerSpecification,
    Vulnerability,
    Threat,
    ThreatsImplementationMethod,
    NegativeConsequence,
    Attacker,
    Capability,
    AttackerScope,
    Tactic,
    Technique,
    ScenarioStep,
    Scenario,
    ISPDNClass,
    GISClass,
    ASUTPClass,
    KIIClass,
    NegativeConsequenceGroup,
    ThreatsImplementationMethodGroup,
    Scope
)

# Register your models here.

admin.site.register(Asset)
admin.site.register(AssetType)
admin.site.register(Vendor)
admin.site.register(Interface)
admin.site.register(AttackerSpecification)
admin.site.register(Vulnerability)
admin.site.register(Threat)

admin.site.register(ThreatsImplementationMethod)
admin.site.register(ThreatsImplementationMethodGroup)
admin.site.register(NegativeConsequence)
admin.site.register(NegativeConsequenceGroup)
admin.site.register(Attacker)
admin.site.register(Capability)
admin.site.register(Scope)
admin.site.register(AttackerScope)
admin.site.register(Tactic)
admin.site.register(Technique)
admin.site.register(ScenarioStep)
admin.site.register(Scenario)
admin.site.register(ISPDNClass)
admin.site.register(GISClass)
admin.site.register(ASUTPClass)
admin.site.register(KIIClass)
