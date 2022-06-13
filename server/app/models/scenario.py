from django.db import models

from app.models import Capability, Interface
from app.models.base_models import BaseModel
from app.models.threats import ThreatsImplementationMethod


class Scenario(BaseModel):
    threat_implementation_method = models.ForeignKey(
        ThreatsImplementationMethod,
        on_delete=models.CASCADE,
        verbose_name='Cпособ реализации',
        null=True
    )

    class Meta:
        verbose_name = 'Сценарий'
        verbose_name_plural = 'Сценарии'


class Tactic(BaseModel):
    number = models.SmallIntegerField('Номер')

    class Meta:
        verbose_name = 'Тактика'
        verbose_name_plural = 'Тактики'

    def __str__(self):
        return f'Т{self.number}. {self.name}'


class Technique(BaseModel):
    name = models.TextField('Название', max_length=1024)
    number = models.SmallIntegerField('Номер')

    tactic = models.ForeignKey(
        Tactic,
        on_delete=models.CASCADE,
        verbose_name='Тактика',
        null=True,
        related_name='techniques'
    )

    capability = models.ForeignKey(
        Capability,
        on_delete=models.CASCADE,
        verbose_name='Возможность нарушителя',
        null=True
    )

    interface = models.ForeignKey(
        Interface,
        on_delete=models.CASCADE,
        verbose_name='Интерфейс',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Техника'
        verbose_name_plural = 'Техники'

    def __str__(self):
        return f'Т{self.tactic.number}.{self.number} {self.name}'


class ScenarioStep(BaseModel):
    step_number = models.IntegerField(verbose_name='Номер шага')
    technique = models.ForeignKey(
        Technique,
        on_delete=models.CASCADE,
        verbose_name='Техника',
        null=True
    )
    scenario = models.ForeignKey(
        Scenario,
        on_delete=models.CASCADE,
        verbose_name='Сценарий'
    )

    class Meta:
        verbose_name = 'Шаг сценария'
        verbose_name_plural = 'Шаги сценария'
        unique_together = ('scenario', 'step_number')