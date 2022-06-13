from typing import List
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q

from app.models import Attacker, ThreatsImplementationMethod, Capability, Threat, AssetType, Tactic, Technique, Asset, \
    Interface, NegativeConsequence
from services.report.report import Report, ReportThreat, ReportThreatImplementation, ReportScenarios
from users_system.models import System as UserSystem


class ReportBuilder:

    def __init__(self, user_system: UserSystem):
        self.system = user_system

    def build(self) -> Report:
        negative_consequences = self.system.negative_consequences.select_related('group').all()
        assets = self.system.assets.all()
        attackers = self.get_actual_attackers(negative_consequences)
        threats = self.get_actual_threats(assets, attackers)
        return Report(
            system=self.system,
            negative_consequences=negative_consequences,
            assets=assets,
            attackers=attackers,
            threats=threats
        )

    def get_actual_threats(self, assets, attackers) -> List[ReportThreat]:
        attackers_capabilities = Capability.objects.filter(attackers__in=attackers).distinct().all()
        threats = Threat.objects.prefetch_related('asset_types__assets').filter(
            asset_types__assets__in=assets,
            implementation_methods__attacker_capability__in=attackers_capabilities,
        ).distinct().all()
        report_threats = []
        for threat in threats:
            implementation_method = self.get_implementation_methods(attackers_capabilities, threat, assets)
            if not implementation_method:
                continue
            report_threats.append(
                ReportThreat(
                    threat=threat,
                    implementations=implementation_method
                )
            )

        return report_threats

    def get_implementation_methods(
            self,
            attackers_capabilities: List[Capability],
            threat: Threat,
            assets: List[Asset]) -> List[ReportThreatImplementation]:

        implementation_methods = ThreatsImplementationMethod.objects.select_related('group').filter(
            attacker_capability__in=attackers_capabilities,
            threats__id__contains=threat.id
        ).distinct().all()
        assets_ids = [asset.id for asset in assets]
        threat_assets = Asset.objects.filter(id__in=assets_ids, asset_type__in=threat.asset_types.all())
        interfaces = Interface.objects.filter(
            asset_type__assets__in=threat_assets
        ).distinct().all()
        results = []
        for implementation_method in implementation_methods:
            scenario = self.get_scenarios(implementation_method.attacker_capability, interfaces)
            if not scenario:
                continue
            results.append(
                ReportThreatImplementation(
                    implementation=implementation_method,
                    scenario=scenario,
                    assets=threat_assets,
                    interfaces=interfaces,
                    attacker_capability=implementation_method.attacker_capability,
                )
            )
        return results

    def get_scenarios(self,
                      attacker_capability: Capability,
                      interfaces: List[Interface]) -> List[ReportScenarios]:

        tactics = Tactic.objects.filter(
            Q(techniques__interface__in=interfaces) | Q(techniques__interface__isnull=True),
            techniques__capability__level__lte=attacker_capability.level,
        ).order_by(
            'number'
        ).annotate(
            techniques_list=ArrayAgg('techniques__number')
        )

        results = []
        for tactic in tactics:
            if not tactic.techniques_list:
                continue
            results.append(
                ReportScenarios(
                    tactic=tactic,
                    techniques=sorted(tactic.techniques_list),
                )
            )
        return results

    def get_actual_attackers(self, negative_consequences: List[NegativeConsequence]) -> List[Attacker]:
        attackers = Attacker.objects.filter(
            attacker_scopes__negative_consequences__in=negative_consequences
        ).distinct().all()
        return attackers
