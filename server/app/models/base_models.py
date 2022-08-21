from django.db import models
from django.utils.translation import gettext_lazy


class BaseModel(models.Model):
    name = models.CharField('Название', max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
