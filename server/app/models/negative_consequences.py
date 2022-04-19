from django.db import models
from app.models.base_models import BaseModel


class NegativeConsequence(BaseModel):
    description = models.TextField('Описание', max_length=511, null=True)

    class Meta:
        verbose_name = 'Негативное последствие'
        verbose_name_plural = 'Негативные последствия'