import pickle
from datetime import datetime
from functools import lru_cache

import xmltodict
from django.core.management.base import BaseCommand, CommandError

from app.models import Vulnerability, Asset, Vendor, AssetType, TypeChoices, PotentialChoices, Attacker, Threat
from pandas import ExcelFile


class Command(BaseCommand):
    help = 'Parser threats from bdu fstec'

    @staticmethod
    def parse_threats_from_xlsx():
        xlsx_data = ExcelFile('threats.xlsx')
        df = xlsx_data.parse(xlsx_data.sheet_names[0])
        return df.to_dict(orient='records')[1:]

    def parse_attackers(self, data: str):
        attackers = set()

        if not isinstance(data, str):
            return attackers

        for attacker_string in data.split(';'):
            attacker_string = attacker_string.strip()
            attacker_type = None
            attacker_potential = None
            if attacker_string.split(' ')[0].lower() == TypeChoices.INSIDER.label.lower():
                attacker_type = TypeChoices.INSIDER
            else:
                attacker_type = TypeChoices.OUTSIDER

            if attacker_string.split(' ')[-2].lower() == 'низким':
                attacker_potential = PotentialChoices.LOW
            elif attacker_string.split(' ')[-2].lower() == 'средним':
                attacker_potential = PotentialChoices.MEDIUM
            elif attacker_string.split(' ')[-2].lower() == 'высоким':
                attacker_potential = PotentialChoices.HIGH

            attacker, _ = Attacker.objects.get_or_create(type=attacker_type, potential=attacker_potential)

            attackers.add(attacker)

        return attackers


    def parse_asset_types(self, data: str):
        asset_types = set()
        for asset_type in data.split(';'):
            asset_type, _ = AssetType.objects.get_or_create(name=asset_type.strip())
            asset_types.add(asset_type)
        return asset_types



        pass

    def handle(self, *args, **options):

        parsed_threats = self.parse_threats_from_xlsx()
        Threat.objects.all().delete()

        for parsed_threat in parsed_threats:
            try:
                attackers = self.parse_attackers(parsed_threat['Unnamed: 3'])
                asset_types = self.parse_asset_types(parsed_threat['Unnamed: 4'])
                threat = Threat(name=parsed_threat['Unnamed: 1'],
                                bdu_id=parsed_threat['Общая информация'],
                                description=parsed_threat['Unnamed: 2'],
                                confidentiality=parsed_threat['Последствия'],
                                integrity=parsed_threat['Unnamed: 6'],
                                availability=parsed_threat['Unnamed: 7'])

                threat.save()
                threat.asset_types.set(asset_types)
                threat.attackers.set(attackers)
                threat.save()
            except Exception as e:
                print(e)
                print(parsed_threat)


        print('sdng')
        self.stdout.write('hui')