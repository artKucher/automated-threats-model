from typing import List

from django.core.management.base import BaseCommand
from pandas import ExcelFile

from app.management.commands.asset_type_mapper import asset_types_mapper
from app.models import AssetType, AttackerSpecification, Threat, ThreatsImplementationMethod, \
    ThreatsImplementationMethodGroup, Capability, CapabilityLevelChoices
from app.models.choices import AttackerTypeChoices, AttackerPotentialChoices

CAPABILITY_LEVEL_MAPPER = {
    1: CapabilityLevelChoices.N1,
    2: CapabilityLevelChoices.N2,
    3: CapabilityLevelChoices.N3,
    4: CapabilityLevelChoices.N4
}


class Command(BaseCommand):
    help = 'Parser threats implementation methods from bdu fstec'

    @staticmethod
    def get_implementation_methods_from_xlsx():
        xlsx_data = ExcelFile('threats_implementation_methods.xlsx')
        df = xlsx_data.parse(xlsx_data.sheet_names[0])
        return df.to_dict(orient='records')[1:]

    def handle(self, *args, **options):
        ThreatsImplementationMethod.objects.all().delete()
        ThreatsImplementationMethodGroup.objects.all().delete()
        records = self.get_implementation_methods_from_xlsx()
        for record in records:
            group = self.parse_implementation_method_groups(record)
            capability = self.parse_attacker_capability(record)
            threats = self.parse_threats(record)
            number = int(record['Идентификатор'].split('.')[2])
            name = record['Наименование']
            implementation_method = ThreatsImplementationMethod(
                number=number,
                name=name,
                group=group,
                attacker_capability=capability
            )
            implementation_method.save()
            implementation_method.threats.set(threats)
            implementation_method.save()


    def parse_threats(self, record) -> List[Threat]:
        threats_data = record['Возможные реализуемые угрозы'].split(';')
        threats = []
        for threat_data in threats_data:
            threat_data = threat_data.replace('_x000D_', '').strip()
            try:
                bdu_id = int(threat_data.split(' ')[0][4:])
            except ValueError:
                return []
            threat = Threat.objects.get(bdu_id=bdu_id)
            threats.append(threat)
        return threats


    def parse_attacker_capability(self, record: dict) -> Capability:
        data = record['Уровень возможностей нарушителя']
        capability_level_number = int(data.split(' ')[0][2:])
        capability_level = CAPABILITY_LEVEL_MAPPER[capability_level_number]
        capability = Capability.objects.get(level=capability_level)
        return capability


    def parse_implementation_method_groups(self, record: dict) -> ThreatsImplementationMethodGroup:
        data = record['Группа способов']
        delimeter_position = data.find(' ')
        number = int(data[:delimeter_position].split('.')[1])
        name = data[delimeter_position:]
        group, _ = ThreatsImplementationMethodGroup.objects.get_or_create(name=name, number=number)
        return group