from django.db import models

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
    class Meta:
        verbose_name = 'Тактика'
        verbose_name_plural = 'Тактики'


class Technique(BaseModel):
    tactic = models.ForeignKey(
        Tactic,
        on_delete=models.CASCADE,
        verbose_name='Тактика',
        null=True
    )
    class Meta:
        verbose_name = 'Техника'
        verbose_name_plural = 'Техники'


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