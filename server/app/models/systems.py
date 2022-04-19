from django.db import models

from app.models import BaseModel
from app.models.choices import SystemTypeChoices


class SystemClass(BaseModel):
    name = models.CharField('Класс', max_length=3)
    type = models.CharField('Тип', max_length=9, choices=SystemTypeChoices.choices, default=SystemTypeChoices.ISPDN)

    class Meta:
        verbose_name = 'Класс системы'
        verbose_name_plural = 'Классы систем'