from django.db import models

from app.models.negative_consequences import NegativeConsequence
from app.models.base_models import BaseModel
from app.models.choices import AttackerTypeChoices, AttackerPotentialChoices, CapabilityLevelChoices


class AttackerSpecification(models.Model):
    type = models.CharField(
        'Тип',
        max_length=8,
        choices=AttackerTypeChoices.choices,
        default=AttackerTypeChoices.INSIDER,
    )
    potential = models.CharField(
        'Потенциал',
        max_length=8,
        choices=AttackerPotentialChoices.choices,
        default=AttackerPotentialChoices.LOW
    )


    def __str__(self):
        return f'{self.get_type_display()} {self.get_potential_display()} '

    class Meta:
        verbose_name = 'Спецификация нарушителя'
        verbose_name_plural = 'Спецификации нарушителей'


class Capability(BaseModel):
    level = models.IntegerField('Уровень', choices=CapabilityLevelChoices.choices, null=True)
    description = models.TextField('Описание', max_length=2048, null=True)

    class Meta:
        verbose_name = 'Возможность нарушителя'
        verbose_name_plural = 'Возможности нарушителей'


class Scope(BaseModel):

    class Meta:
        verbose_name = 'Возможная цель нарушителя'
        verbose_name_plural = 'Возможные цели нарушителей'


class Attacker(BaseModel):
    attacker_specification = models.ManyToManyField(AttackerSpecification, verbose_name='Спецификации нарушителей')
    capability = models.ForeignKey(
        Capability,
        on_delete=models.CASCADE,
        verbose_name='Возможности',
        null=True,
        related_name='attackers'
    )

    class Meta:
        verbose_name = 'Нарушитель'
        verbose_name_plural = 'Нарушители'


class AttackerScope(models.Model):
    scope = models.ForeignKey(Scope, verbose_name='Цель', on_delete=models.CASCADE)
    negative_consequences = models.ManyToManyField(NegativeConsequence, verbose_name='Негативные последствия')
    attacker = models.ForeignKey(
        Attacker,
        verbose_name='Нарушитель',
        on_delete=models.CASCADE,
        related_name='attacker_scopes',
    )

    class Meta:
        verbose_name = 'Цель нарушителя'
        verbose_name_plural = 'Цели нарушителей'

    def __str__(self):
        negative_consequences_numbers = ', '.join([
            negative_consequence.get_number() for negative_consequence in self.negative_consequences.all()
        ])
        return f'{self.scope} {negative_consequences_numbers}'
