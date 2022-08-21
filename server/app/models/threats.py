from django.db import models

from app.models.assets import AssetType, Interface
from app.models.attackers import AttackerSpecification, Capability
from app.models.base_models import BaseModel


class Threat(BaseModel):
    name = models.CharField('Название', max_length=1023)
    bdu_id = models.IntegerField('Идентификатор УБИ', null=True)
    description = models.TextField('Описание', max_length=1023, null=True)
    asset_types = models.ManyToManyField(AssetType, verbose_name='Типы объектов')
    attackers = models.ManyToManyField(AttackerSpecification, verbose_name='Спецификация нарушителя')
    confidentiality = models.BooleanField('Нарушает конфиденциальность', default=False)
    integrity = models.BooleanField('Нарушает целостность', default=False)
    availability = models.BooleanField('Нарушает доступность', default=False)

    class Meta:
        verbose_name = 'Угроза'
        verbose_name_plural = 'Угрозы'

    def __str__(self):
        return f'УБИ{self.bdu_id}. {self.name}'


class ThreatsImplementationMethodGroup(BaseModel):
    number = models.SmallIntegerField('Номер группы')

    class Meta:
        verbose_name = 'Группа способов реализации угроз'
        verbose_name_plural = 'Группы способов реализации угроз'

    def __str__(self):
        return f'СП.{self.number} {self.name}'


class ThreatsImplementationMethod(BaseModel):
    number = models.SmallIntegerField('Номер')
    group = models.ForeignKey(
        ThreatsImplementationMethodGroup,
        on_delete=models.CASCADE,
        verbose_name='Группа'
    )

    attacker_capability = models.ForeignKey(Capability,
                                            on_delete=models.CASCADE,
                                            verbose_name='Возможность нарушителя',
                                            null=True)
    asset_interface = models.ForeignKey(Interface,
                                        on_delete=models.CASCADE,
                                        verbose_name='Используемый интерфейс',
                                        null=True)
    threats = models.ManyToManyField(
        Threat,
        verbose_name='Угрозы',
        related_name='implementation_methods')


    class Meta:
        verbose_name = 'Cпособ реализации'
        verbose_name_plural = 'Способы реализации'

    def __str__(self):
        return f'СП.{self.group.number}.{self.number} {self.name}'