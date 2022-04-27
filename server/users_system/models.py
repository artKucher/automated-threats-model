from django.db import models

from app.models import ISPDNClass, GISClass, ASUTPClass, KIIClass
from app.models.assets import Asset
from app.models.base_models import BaseModel
from app.models.negative_consequences import NegativeConsequence


class System(BaseModel):
    ispdn_classes = models.ManyToManyField(ISPDNClass, verbose_name='Классы ИСПДн')
    gis_classes = models.ManyToManyField(GISClass, verbose_name='Классы ГИС')
    asutp_classes = models.ManyToManyField(ASUTPClass, verbose_name='Классы АСУТП')
    kii_classes = models.ManyToManyField(KIIClass, verbose_name='Классы КИИ')

    assets = models.ManyToManyField(Asset, verbose_name='Объекты')

    class Meta:
        verbose_name = 'Система'
        verbose_name_plural = 'Системы'

