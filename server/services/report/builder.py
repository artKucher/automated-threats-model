from typing import List

from app.models import Attacker, ThreatsImplementationMethod, Capability, Threat, AssetType, Tactic, Technique, Asset, \
    Interface
from services.report.report import Report, ReportThreat, ReportThreatImplementation, ReportScenarios
from users_system.models import System as UserSystem


class ReportBuilder:

    def __init__(self, user_system: UserSystem):
        self.system = user_system

    def build(self) -> Report:
        negative_consequences = self.system.negative_consequences.all()
        assets = self.system.assets.all()
        attackers = self.get_actual_attackers()
        threats = self.get_actual_threats(assets, attackers)
        return Report(
            negative_consequences=negative_consequences,
            assets=assets,
            attackers=attackers,
            threats=threats
        )

    def get_actual_threats(self, assets, attackers) -> List[ReportThreat]:
        threats = Threat.objects.filter(asset_types__assets__in=assets).all()
        report_threats = []
        for threat in threats:
            implementation_method = self.get_implementation_methods(attackers, threat, assets)
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
            attackers: List[Attacker],
            threat: Threat,
            assets: List[Asset]) -> List[ReportThreatImplementation]:

        attackers_capabilities = Capability.objects.filter(attackers__in=attackers).all()
        implementation_methods = ThreatsImplementationMethod.objects.filter(
            attacker_capability__in=attackers_capabilities,
            threats=threat
        ).all()
        assets_ids = [asset.id for asset in assets]
        threat_assets = Asset.objects.filter(id__in=assets_ids, asset_type__in=threat.asset_types.all())
        results = []
        for implementation_method in implementation_methods:
            scenario = self.get_scenarios(implementation_method, threat_assets)
            if not scenario:
                continue
            results.append(
                ReportThreatImplementation(
                    implementation=implementation_method,
                    scenario=scenario,
                    assets=threat_assets,
                )
            )
        return results

    def get_scenarios(self,
                      implementation_method: ThreatsImplementationMethod,
                      assets: List[Asset]) -> List[ReportScenarios]:
        tactics = Tactic.objects.order_by('number').all()
        results = []
        interfaces = Interface.objects.filter(
            asset_type__assets__in=assets
        )
        for tactic in tactics:
            techniques = Technique.objects.filter(
                tactic=tactic,
                capability=implementation_method.attacker_capability,
                interface__in=interfaces,
            )
            if not techniques:
                continue
            results.append(
                ReportScenarios(
                    tactic=tactic,
                    techniques=techniques,
                )
            )
        return results

    def get_actual_attackers(self) -> List[Attacker]:
        attackers = Attacker.objects.filter(
            scopes__negative_consequences__in=self.system.negative_consequences.all()
        ).all()
        return attackers
