import markdown
from django.contrib import admin
# Register your models here.
from django.http import HttpResponse
from xhtml2pdf import pisa

from app.models import Vulnerability, Threat
from users_system.models import System


class SystemAdmin(admin.ModelAdmin):
    filter_horizontal = ('assets',)

    base_html = '''<html> 
                     <head> 
                         <meta content="text/html; charset=utf-8" http-equiv="Content-Type"> 
                         <style type="text/css"> 
                             @page { size: A4; margin: 1cm; }
                             @font-face { font-family: Arial; src: url(/server/static/arial.ttf); }
                             @font-face { font-family: Arial-bold; src: url(/server/static/arial_bold.ttf); }
                             strong { color: black; font-family: Arial-bold; }
                             * { color: black; font-family: Arial; }
                         </style> 
                     </head> 
                     <body> 
                     '''
    base_html_end = '''
    </body> 
                 </html>'''

    def make_report(self, request, queryset):
        report_text = ''
        systems = queryset.all()
        for system in systems:
            report_text += f'#{system.name}. {system.get_type_display()}\n'
            report_text += f'##Объекты:\n'
            for asset in system.assets.all():
                report_text+= f'**{asset.name}**. Тип: {asset.asset_type}. Вендор: {asset.vendor}\n\n'
                report_text += f'###Уязвимости:\n\n'
                vulnerabilities = Vulnerability.objects.filter(asset=asset).all()
                for count, vulnerability in enumerate(vulnerabilities):
                    report_text += f'{count+1}) {vulnerability.name}\n'
                    report_text += f' **Описание:** {vulnerability.description}\n'
                    report_text += f' **CVSS 2.0:** {vulnerability.cvss_v2}\n' if vulnerability.cvss_v2 else ''
                    report_text += f' **CVSS 3.0:** {vulnerability.cvss_v3}\n' if vulnerability.cvss_v3 else ''
                    report_text += f' **Способ устранения:** {vulnerability.bdu_countermeasure_advice}\n'
                    report_text += f' **Источники:** {vulnerability.source_link}\n\n'

                report_text += f'\nУгрозы:\n\n'
                threats = Threat.objects.filter(asset_types__in=[asset.asset_type]).all()
                for count, threat in enumerate(threats):
                    report_text += f'{count+1}) {threat.name}\n'
                    report_text += f' **Описание:** {threat.description}\n'
                    report_text += f' **Угроза К|Ц|Д:** {threat.confidentiality}|{threat.integrity}|{threat.availability}\n'
                    report_text += f' **Нарушители:** {", ".join([str(attacker) for attacker in threat.attackers.all()])}\n\n' \
                        if threat.attackers.all() else ''
                report_text += f'\n____________________________________________\n\n'
            report_text += f'____________________________________________\n\n'

        #print(report_text, flush=True)
        report_html = markdown.markdown(report_text, extensions=['footnotes', 'nl2br'])

        response = HttpResponse(content_type="application/pdf")
        # create a pdf
        report = self.base_html + report_html + self.base_html_end
        #print(report, flush=True)
        pisa_status = pisa.CreatePDF(report, dest=response, encoding='utf-8')

        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + report_html + '</pre>')

        return response
    make_report.short_description = "Выгрузить отчёт"

    actions = [make_report]

admin.site.register(System, SystemAdmin)


