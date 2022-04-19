from django.db import models

from app.models.assets import Asset
from app.models.base_models import BaseModel
from app.models.negative_consequences import NegativeConsequence
from app.models.systems import SystemClass


class System(BaseModel):
    system_class = models.ForeignKey(
        SystemClass,
        on_delete=models.CASCADE,
        verbose_name='Класс системы',
        null=True
    )
    assets = models.ManyToManyField(Asset, verbose_name='Объекты')
    negative_consequences = models.ManyToManyField(NegativeConsequence, verbose_name='Негативные последствия')

    class Meta:
        verbose_name = 'Система'
        verbose_name_plural = 'Системы'

