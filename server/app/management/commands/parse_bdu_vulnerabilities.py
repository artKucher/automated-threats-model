import pickle
from datetime import datetime

from django.core.management.base import BaseCommand

from app.management.commands.asset_type_mapper import asset_types_mapper
from app.models import Vulnerability, Asset, Vendor, AssetType


class Command(BaseCommand):
    help = 'Parser vulnerabilities form bdu fstec'

    def parse_xml(self, xml_data):
        print('parse it')
        # parsed_value = xmltodict.parse(xml_data)
        # with open('cache_parsed_xml.json', 'wb') as f:
        #     pickle.dump(parsed_value, f)
        with open('cache_parsed_xml.json', 'rb') as f:
            parsed_value = pickle.load(f)
            return parsed_value

    def handle(self, *args, **options):
        xml_data = ''
        with open('vulnerabilities.xml') as f:
            xml_data = f.read()

        parsed_vulnerabilities = self.parse_xml(xml_data)['vulnerabilities']['vul']

        Vulnerability.objects.all().delete()

        for parsed_vulnerability in parsed_vulnerabilities:
            try:
                parsed_asset = parsed_vulnerability['vulnerable_software']['soft']
                if isinstance(parsed_asset, list):
                    parsed_asset = parsed_asset[0]
                vendor, _ = Vendor.objects.get_or_create(name=parsed_asset['vendor'])

                parsed_asset_type = parsed_asset['types']['type']
                if isinstance(parsed_asset_type, list):
                    parsed_asset_type = parsed_asset_type[0]
                asset_type_name = asset_types_mapper[parsed_asset_type]
                asset_type, _ = AssetType.objects.get_or_create(name=asset_type_name)


                asset, _ = Asset.objects.get_or_create(name=parsed_asset['name'],
                                                       asset_type=asset_type,
                                                       vendor=vendor)

                vulnerability = Vulnerability(name=parsed_vulnerability['name'],
                                              bdu_id=parsed_vulnerability['identifier'],
                                              description=parsed_vulnerability['description'],
                                              cvss_v2=parsed_vulnerability['cvss']['vector']['#text'],
                                              cvss_v2_score=parsed_vulnerability['cvss']['vector']['@score'],
                                              severity=parsed_vulnerability['severity'],
                                              bdu_countermeasure_advice=parsed_vulnerability['solution'],
                                              source_link=parsed_vulnerability['sources'],
                                              discovery_date=datetime.strptime(parsed_vulnerability['identify_date'],
                                                                               '%d.%m.%Y'),
                                              asset=asset)
                vulnerability.save()
            except Exception as e:
                print(parsed_vulnerability['identifier'])

        print('sdng')