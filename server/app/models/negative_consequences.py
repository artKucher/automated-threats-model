from django.db import models
from app.models.base_models import BaseModel


class NegativeConsequenceGroup(BaseModel):
    number = models.SmallIntegerField('Номер группы')

    class Meta:
        verbose_name = 'Группа негативных последствий'
        verbose_name_plural = 'Группы негативных последствий'

    def __str__(self):
        return f'У{self.number} {self.name}'


class NegativeConsequence(BaseModel):
    group = models.ForeignKey(
        NegativeConsequenceGroup,
        on_delete=models.CASCADE,
        verbose_name='Группа'
    )
    number = models.SmallIntegerField('Номер')
    description = models.TextField('Описание', max_length=511, null=True)

    @property
    def full_name(self):
        return str(self)

    class Meta:
        verbose_name = 'Негативное последствие'
        verbose_name_plural = 'Негативные последствия'

    def __str__(self):
        return f'У{self.group.number}.{self.number} {self.name}'

    def get_number(self):
        return f'У{self.group.number}.{self.number}'
