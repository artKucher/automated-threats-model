from io import BytesIO
from typing import Any
from typing import List as ListType

from odf.style import Style, TextProperties, ListLevelProperties
from odf.text import P, Span, H, ListStyle, List, ListItem, ListLevelStyleNumber

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
                implementation_name = P(text=implementation.implementation)
                self.document.text.addElement(implementation_name)
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
        assets_block_header = H(outlinelevel=1, stylename=self.h2style, text=f"Объекты:")
        assets_list = self.generate_numbered_list(self.report.assets)
        negative_consequences_block_header = H(outlinelevel=1, stylename=self.h2style, text=f"Негативные последствия:")
        negative_consequences_list = self.generate_numbered_list(self.report.negative_consequences)

        self.document.text.addElement(system_header)
        self.document.text.addElement(assets_block_header)
        self.document.text.addElement(assets_list)
        self.document.text.addElement(negative_consequences_block_header)
        self.document.text.addElement(negative_consequences_list)

    def generate_numbered_list(self, collection: ListType[Any]):
        assets_list = List(stylename=self.numberedliststyle)
        for asset in collection:
            list_item = ListItem()
            list_item.addElement(P(text=asset))
            assets_list.addElement(list_item)
        return assets_list
