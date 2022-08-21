from dataclasses import dataclass
from typing import List, Optional
from app.models import Asset, NegativeConsequence, Attacker, ThreatsImplementationMethod, Threat, Technique, Tactic, \
    Interface, Capability
from users_system.models import System as UserSystem


@dataclass
class ReportScenarios:
    tactic: Tactic
    techniques: List[Technique]


@dataclass
class ReportThreatImplementation:
    implementation: ThreatsImplementationMethod
    scenario: List[ReportScenarios]
    assets: Optional[List[Asset]]
    interfaces: List[Interface]
    attacker_capability: List[Capability]


@dataclass
class ReportThreat:
    threat: Threat
    implementations: List[ReportThreatImplementation]


@dataclass
class Report:
    system: UserSystem
    negative_consequences: List[NegativeConsequence]
    assets: List[Asset]
    attackers: List[Attacker]
    threats: List[ReportThreat]


