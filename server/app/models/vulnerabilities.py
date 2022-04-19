from django.db import models

from app.models.assets import Asset, Interface
from app.models.base_models import BaseModel
from app.models.choices import AttackerTypeChoices


class Vulnerability(BaseModel):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, verbose_name='Объект', null=True)

    name = models.CharField('Название', max_length=1023)
    interface = models.ForeignKey(Interface, on_delete=models.DO_NOTHING, verbose_name='Интерфейс', null=True)
    type = models.CharField('Тип', max_length=8, choices=AttackerTypeChoices.choices, default=AttackerTypeChoices.INSIDER)
    bdu_id = models.CharField('Идентификатор БДУ', max_length=14, null=True)
    description = models.TextField('Описание', max_length=511, null=True)
    discovery_date = models.DateField('Дата выявления', null=True)
    cvss_v2 = models.CharField('CVSS 2.0', max_length=63, null=True)
    cvss_v3 = models.CharField('CVSS 3.0', max_length=63, null=True)
    cvss_v2_score = models.FloatField('CVSS 2.0 Оценка', null=True)
    cvss_v3_score = models.FloatField('CVSS 3.0 Оценка', null=True)
    severity = models.CharField('Критичность', max_length=255, null=True)
    bdu_countermeasure_advice = models.TextField('Возможный способ устранения', max_length=511, null=True)
    source_link = models.TextField('Ссылка на источник', max_length=3000, null=True)

    class Meta:
        verbose_name = 'Уязвимость'
        verbose_name_plural = 'Уязвимости'