from django.db import models

from app.models import ISPDNClass, GISClass, ASUTPClass, KIIClass
from app.models.assets import Asset
from app.models.base_models import BaseModel
from app.models.negative_consequences import NegativeConsequence


class System(BaseModel):
    ispdn_classes = models.ManyToManyField(ISPDNClass, verbose_name='Классы ИСПДн', blank=True)
    gis_classes = models.ManyToManyField(GISClass, verbose_name='Классы ГИС', blank=True)
    asutp_classes = models.ManyToManyField(ASUTPClass, verbose_name='Классы АСУТП', blank=True)
    kii_classes = models.ManyToManyField(KIIClass, verbose_name='Классы КИИ', blank=True)

    assets = models.ManyToManyField(Asset, verbose_name='Объекты', blank=True)
    negative_consequences = models.ManyToManyField(
        NegativeConsequence,
        verbose_name='Негативные последствия',
        blank=True
    )

    class Meta:
        verbose_name = 'Система'
        verbose_name_plural = 'Системы'

