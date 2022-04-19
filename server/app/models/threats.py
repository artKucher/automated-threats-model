from django.db import models

from app.models.assets import AssetType, Interface
from app.models.attackers import AttackerSpecification, Capability
from app.models.base_models import BaseModel


class Threat(BaseModel):
    name = models.CharField('Название', max_length=1023)
    bdu_id = models.IntegerField('Идентификатор УБИ>', null=True)
    description = models.TextField('Описание', max_length=1023, null=True)
    asset_types = models.ManyToManyField(AssetType, verbose_name='Типы объектов')
    attackers = models.ManyToManyField(AttackerSpecification, verbose_name='Спецификация нарушителя')
    confidentiality = models.BooleanField('Нарушает конфиденциальность', default=False)
    integrity = models.BooleanField('Нарушает целостность', default=False)
    availability = models.BooleanField('Нарушает доступность', default=False)

    class Meta:
        verbose_name = 'Угроза'
        verbose_name_plural = 'Угрозы'


class ThreatsImplementationMethod(BaseModel):
    description = models.TextField('Описание', max_length=511, null=True)
    attacker_capability = models.ForeignKey(Capability,
                                            on_delete=models.CASCADE,
                                            verbose_name='Возможность нарушителя',
                                            null=True)
    asset_interface = models.ForeignKey(Interface,
                                        on_delete=models.CASCADE,
                                        verbose_name='Используемый интерфейс',
                                        null=True)


    class Meta:
        verbose_name = 'Cпособ реализации'
        verbose_name_plural = 'Способы реализации'