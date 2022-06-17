import io
import random
from io import BytesIO
from typing import Any
from typing import List as ListType

from matplotlib import pyplot as plt
from odf.draw import Image, Frame
from odf.style import Style, TextProperties, ListLevelProperties, GraphicProperties
from odf.text import P, H, ListStyle, List, ListItem, ListLevelStyleNumber

from app.models import NegativeConsequenceGroup, AssetType
from services.report.report import Report
from odf.opendocument import OpenDocumentText


class ReportPrinter:
    def __init__(self, report: Report):
        self.report = report
        self.buffer = BytesIO()
        self.document = OpenDocumentText()

        self.h1style = Style(name="Heading 1", family="paragraph")
        self.h1style.addElement(TextProperties(attributes={'fontsize': "18pt", 'fontweight': "bold"}))
        self.h2style = Style(name="Heading 2", family="paragraph")
        self.h2style.addElement(TextProperties(attributes={'fontsize': "14pt", 'fontweight': "bold"}))

        self.numberedliststyle = ListStyle(name="NumberedList")
        level = 1
        numberedlistproperty = ListLevelStyleNumber(
            level=str(level), numsuffix=".", startvalue=1)
        numberedlistproperty.setAttribute('numsuffix', ".")
        numberedlistproperty.addElement(ListLevelProperties(
            minlabelwidth="%fcm" % (level - .2)))
        self.numberedliststyle.addElement(numberedlistproperty)

        image_style = Style(name='frstyle', parentstylename="Graphics", family="graphic")
        image_style.addElement(GraphicProperties(verticalrel="paragraph",
                                             horizontalrel="paragraph"))
        self.image_style = image_style
        self.document.automaticstyles.addElement(image_style)

        self.document.styles.addElement(self.h1style)
        self.document.styles.addElement(self.h2style)
        self.document.styles.addElement(self.numberedliststyle)

    def print(self):

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        self.generate_main_page()
        self.generate_actual_attackers_page()
        self.generate_threats_page()
        self.document.write(self.buffer)

        return self.buffer

    def generate_threats_page(self):
        header = H(outlinelevel=1, stylename=self.h1style, text=f"Угрозы")
        self.document.text.addElement(header)
        for threat in self.report.threats:
            threat_name = H(outlinelevel=1, stylename=self.h2style, text=f"{threat.threat}")
            self.document.text.addElement(threat_name)
            self.document.text.addElement(P(text='Способы реализации:'))
            for implementation in threat.implementations:
                self.document.text.addElement(P(text=''))
                self.document.text.addElement(P(text=implementation.implementation))
                capability_text = (
                    f'Требуемый уровень возможностей нарушителя: '
                    f'{implementation.attacker_capability}'
                )
                self.document.text.addElement(P(text=capability_text))
                interfaces_names = [str(interface) for interface in implementation.interfaces]
                interfaces_list = ', '.join(interfaces_names)
                interfaces_text = (
                    f'Интерфейсы: {interfaces_list}'
                )
                self.document.text.addElement(P(text=interfaces_text))
                for scenario_step in implementation.scenario:
                    tactic = P(text=f'{scenario_step.tactic}')
                    techniques_list = [
                        f'T{scenario_step.tactic.number}.{technique_number}'
                        for technique_number in scenario_step.techniques
                    ]
                    techniques = P(text=', '.join(techniques_list))
                    self.document.text.addElement(tactic)
                    self.document.text.addElement(techniques)

    def generate_actual_attackers_page(self):
        header = H(outlinelevel=1, stylename=self.h1style, text=f"Актуальные нарушители")
        actual_attackers_list = self.generate_numbered_list(self.report.attackers)
        self.document.text.addElement(header)
        self.document.text.addElement(actual_attackers_list)

    def generate_main_page(self):
        system_header = H(outlinelevel=1, stylename=self.h1style, text=f"Cистема: {self.report.system.name}")
        self.document.text.addElement(system_header)
        self.add_ispdn_classes_info()
        self.add_gis_classes_info()
        self.add_asutp_classes_info()
        self.add_kii_classes_info()

        self.document.text.addElement(
            H(outlinelevel=1, stylename=self.h2style, text=f"Объектов: {self.report.assets.count()} шт.")
        )
        labels = []
        sizes = []
        for type in AssetType.objects.all():
            assets_count = self.report.system.assets.filter(asset_type=type).count()
            if assets_count:
                labels.append(str(type))
                sizes.append(
                    assets_count
                )

        chart = self.draw_chart(
            labels=labels,
            sizes=sizes,
        )
        self.add_chart(chart)

        self.document.text.addElement(
            H(
                outlinelevel=1,
                stylename=self.h2style,
                text=f"Негативных последствий: {self.report.negative_consequences.count()} шт."
            )
        )
        labels = []
        sizes = []
        for group in NegativeConsequenceGroup.objects.all():
            labels.append(str(group))
            group_negative_consequences_count = self.report.system.negative_consequences.filter(group=group).count()
            sizes.append(
                group_negative_consequences_count
            )
        chart = self.draw_chart(
            labels=labels,
            sizes=sizes,
        )
        self.add_chart(chart)


        assets_block_header = H(outlinelevel=1, stylename=self.h2style, text=f"Объекты:")
        assets_list = self.generate_numbered_list(self.report.assets)
        negative_consequences_block_header = H(outlinelevel=1, stylename=self.h2style, text=f"Негативные последствия:")
        negative_consequences_list = self.generate_numbered_list(self.report.negative_consequences)

        self.document.text.addElement(assets_block_header)
        self.document.text.addElement(assets_list)
        self.document.text.addElement(negative_consequences_block_header)
        self.document.text.addElement(negative_consequences_list)

    def add_chart(self, chart):
        photoframe = Frame(width="260pt", height="200pt", stylename=self.image_style)
        href = self.document.addPicture(filename=str(random.randint(0, 9999)), content=chart)
        photoframe.addElement(Image(href=href))
        p = P()
        p.addElement(photoframe)
        self.document.text.addElement(p)
        self.document.text.addElement(P(text=''))
        self.document.text.addElement(P(text=''))
        self.document.text.addElement(P(text=''))
        self.document.text.addElement(P(text=''))
        self.document.text.addElement(P(text=''))
        self.document.text.addElement(P(text=''))
        self.document.text.addElement(P(text=''))
        self.document.text.addElement(P(text=''))
        self.document.text.addElement(P(text=''))
        self.document.text.addElement(P(text=''))
        self.document.text.addElement(P(text=''))
        self.document.text.addElement(P(text=''))
        self.document.text.addElement(P(text=''))
        self.document.text.addElement(P(text=''))

    def draw_chart(self, labels, sizes):

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        buf = io.BytesIO()
        plt.savefig(buf)
        return buf.getvalue()

    def add_ispdn_classes_info(self):
        if self.report.system.ispdn_classes.exists():
            ispdn_specifications = [
                str(ispdn.get_specification_display()) for ispdn in self.report.system.ispdn_classes.all()
            ]
            ispdn_type = self.report.system.ispdn_classes.all()[0].get_type_display()
            ispdn_protection_level = self.report.system.ispdn_classes.all()[0].get_protection_level_display()
            text = f"ИСПДН: {ispdn_type}, {ispdn_protection_level}, {'; '.join(ispdn_specifications)}"
            self.document.text.addElement(P(text=text))

    def add_gis_classes_info(self):
        if self.report.system.gis_classes.exists():
            gis_specifications = [
                str(gis.get_specification_display()) for gis in self.report.system.gis_classes.all()
            ]
            gis_size = self.report.system.gis_classes.all()[0].get_size_display()
            gis_protection_class = self.report.system.gis_classes.all()[0].get_protection_class_display()
            text = f"ГИС: {gis_specifications}, {gis_size}, {';'.join(gis_protection_class)}"
            self.document.text.addElement(P(text=text))

    def add_asutp_classes_info(self):
        if self.report.system.asutp_classes.exists():
            asutp_specifications = [
                str(asutp.get_specification_display()) for asutp in self.report.system.asutp_classes.all()
            ]
            asutp_protection_class = self.report.system.gis_classes.all()[0].get_protection_class_display()
            text = f"АСУТП: {asutp_protection_class}, {';'.join(asutp_specifications)}"
            self.document.text.addElement(P(text=text))

    def add_kii_classes_info(self):
        if self.report.system.kii_classes.exists():
            kii_specifications = [
                str(kii.get_specification_display()) for kii in self.report.system.kii_classes.all()
            ]
            kii_significance_attribute = self.report.system.kii_classes.all()[0].get_significance_attribute_display()
            text = f"КИИ: {kii_significance_attribute}, {';'.join(kii_specifications)}"
            self.document.text.addElement(P(text=text))

    def generate_numbered_list(self, collection: ListType[Any]):
        assets_list = List(stylename=self.numberedliststyle)
        for asset in collection:
            list_item = ListItem()
            list_item.addElement(P(text=asset))
            assets_list.addElement(list_item)
        return assets_list
