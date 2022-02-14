from django.db import models
from django.utils.translation import gettext_lazy


class BaseModel(models.Model):
    name = models.CharField('Название', max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Asset(BaseModel):
    pass

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'


class Interface(BaseModel):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, verbose_name='Объект')

    class Meta:
        verbose_name = 'Интерфейс'
        verbose_name_plural = 'Интерфейсы'


class PotentialChoices(models.TextChoices):
    """ ФСБ потенциал нарушителя """
    HIGH = 'HIGH', 'Высокий'
    MEDIUM = 'MEDIUM', 'Средний'
    LOW = 'LOW', 'Низкий'


class CapabilityLevelChoices(models.TextChoices):
    """ ФСТЭК уровень возможностей нарушителя """
    N4 = 'N4', 'Н4'
    N3 = 'N3', 'Н3'
    N2 = 'N2', 'Н2'
    N1 = 'N1', 'Н1'


class Capabilities(models.Model):
    potential = models.CharField('Потенциал', max_length=8, choices=PotentialChoices.choices, default=PotentialChoices.LOW)
    level = models.CharField('Уровень', max_length=2, choices=CapabilityLevelChoices.choices, default=CapabilityLevelChoices.N4)

    def __str__(self):
        return f'{self.potential}, {self.level}'

    class Meta:
        verbose_name = 'Возможность нарушителя'
        verbose_name_plural = 'Возможности нарушителя'


class TypeChoices(models.TextChoices):
    INSIDER = 'INSIDER', 'Внутренний'
    OUTSIDER = 'OUTSIDER', 'Внешний'


class Attacker(BaseModel):
    type = models.CharField('Тип', max_length=8, choices=TypeChoices.choices, default=TypeChoices.INSIDER)
    capabilities = models.ManyToManyField(Capabilities, verbose_name='Возможности')

    class Meta:
        verbose_name = 'Нарушитель'
        verbose_name_plural = 'Нарушители'


class Vulnerability(BaseModel):
    interface = models.ForeignKey(Interface, on_delete=models.DO_NOTHING, verbose_name='Интерфейс')
    type = models.CharField('Тип', max_length=8, choices=TypeChoices.choices, default=TypeChoices.INSIDER)

    class Meta:
        verbose_name = 'Уязвимость'
        verbose_name_plural = 'Уязвимости'


class Threat(BaseModel):
    vulnerability = models.ForeignKey(Vulnerability, on_delete=models.DO_NOTHING, verbose_name='Уязвимость')
    potential = models.CharField('Потенциал нарушителя', max_length=8, choices=PotentialChoices.choices, default=PotentialChoices.LOW)

    class Meta:
        verbose_name = 'Угроза'
        verbose_name_plural = 'Угрозы'