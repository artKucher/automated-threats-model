from django.db import models

from app.models import NegativeConsequence
from app.models.choices import ISPDNTypeChoices, ISPDNSpecificationChoices, GISSpecificationChoices, \
    GISSizeChoices, ProtectionClassChoices, ASUTPSpecificationChoices, KIISpecificationChoices, ProtectionLevelChoices, \
    SignificanceAttributeChoices


class SystemsClassManager(models.Manager):
    def negative_consequences_ids(self):
        return self.get_queryset().select_related(
            'negative_consequences'
        ).values_list(
            'negative_consequences__id',
            flat=True
        )


class BaseSystemClass(models.Model):
    objects = SystemsClassManager()
    negative_consequences = models.ManyToManyField(
        NegativeConsequence,
        verbose_name='Негативные последствия'
    )
    class Meta:
        abstract = True


class ISPDNClass(BaseSystemClass):
    type = models.CharField(
        'Тип',
        max_length=9,
        choices=ISPDNTypeChoices.choices,
        default=ISPDNTypeChoices.PUBLIC
    )

    specification = models.CharField(
        'Спецификация',
        max_length=44,
        choices=ISPDNSpecificationChoices.choices
    )

    protection_level = models.CharField(
        'Уровень защищенности',
        max_length=3,
        choices=ProtectionLevelChoices.choices,
        default=ProtectionLevelChoices.UZ1
    )

    def __str__(self):
        return f'{self.get_type_display()} {self.get_specification_display()} {self.get_protection_level_display()}'

    class Meta:
        verbose_name = 'ИСПДН'
        verbose_name_plural = 'ИСПДН'


class GISClass(BaseSystemClass):
    size = models.CharField(
        'Масштаб',
        max_length=9,
        choices=GISSizeChoices.choices,
        default=GISSizeChoices.REGIONAL
    )

    protection_class = models.CharField(
        'Класс защищенности',
        max_length=2,
        choices=ProtectionClassChoices.choices,
        default=ProtectionClassChoices.K1
    )

    specification = models.CharField(
        'Спецификация',
        max_length=44,
        choices=GISSpecificationChoices.choices
    )

    def __str__(self):
        return f'{self.get_size_display()} {self.get_specification_display()} {self.get_protection_class_display()}'

    class Meta:
        verbose_name = 'ГИС'
        verbose_name_plural = 'ГИС'


class ASUTPClass(BaseSystemClass):
    protection_class = models.CharField(
        'Класс защищенности',
        max_length=2,
        choices=ProtectionClassChoices.choices,
        default=ProtectionClassChoices.K1
    )

    specification = models.CharField(
        'Спецификация',
        max_length=44,
        choices=ASUTPSpecificationChoices.choices
    )

    def __str__(self):
        return f'{self.get_specification_display()} {self.get_protection_class_display()}'

    class Meta:
        verbose_name = 'АСУТП'
        verbose_name_plural = 'АСУТП'


class KIIClass(BaseSystemClass):
    specification = models.CharField(
        'Спецификация',
        max_length=44,
        choices=KIISpecificationChoices.choices
    )

    significance_attribute = models.CharField(
        'Критерий значимости',
        max_length=13,
        choices=SignificanceAttributeChoices.choices,
        default=SignificanceAttributeChoices.KZ1
    )

    def __str__(self):
        return f'{self.get_specification_display()} {self.get_significance_attribute_display()}'

    class Meta:
        verbose_name = 'КИИ'
        verbose_name_plural = 'КИИ'
