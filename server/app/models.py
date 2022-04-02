from django.db import models
from django.utils.translation import gettext_lazy


class BaseModel(models.Model):
    name = models.CharField('Название', max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class AssetType(BaseModel):
    name = models.CharField('Название', max_length=511)
    pass

    class Meta:
        verbose_name = 'Тип объекта'
        verbose_name_plural = 'Типы объектов'


class Vendor(BaseModel):
    pass

    class Meta:
        verbose_name = 'Вендор'
        verbose_name_plural = 'Вендоры'


class Asset(BaseModel):
    asset_type = models.ForeignKey(AssetType, on_delete=models.CASCADE, verbose_name='Тип объекта', null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, verbose_name='Вендор', null=True)

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'


class System(BaseModel):
    class TypeChoices(models.TextChoices):
        ISPDN = 'ISPDN', 'ИСПДн'
        ASUTP = 'ASUTP', 'АСУТП'

    type = models.CharField('Тип', max_length=8, choices=TypeChoices.choices)
    assets = models.ManyToManyField(Asset, verbose_name='Объекты')

    class Meta:
        verbose_name = 'Система'
        verbose_name_plural = 'Системы'


class Interface(BaseModel):
    asset_type = models.ForeignKey(AssetType, on_delete=models.CASCADE, verbose_name='Тип объекта')

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


class TypeChoices(models.TextChoices):
    INSIDER = 'INSIDER', 'Внутренний'
    OUTSIDER = 'OUTSIDER', 'Внешний'


class Attacker(models.Model):
    type = models.CharField('Тип', max_length=8, choices=TypeChoices.choices, default=TypeChoices.INSIDER)
    potential = models.CharField('Потенциал', max_length=8, choices=PotentialChoices.choices, default=PotentialChoices.LOW)
    level = models.CharField('Уровень', max_length=2, choices=CapabilityLevelChoices.choices, null=True)

    def __str__(self):
        return f'{self.get_type_display()} {self.get_potential_display()} {self.get_level_display() or ""}'

    class Meta:
        verbose_name = 'Нарушитель'
        verbose_name_plural = 'Нарушители'


class Vulnerability(BaseModel):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, verbose_name='Объект', null=True)

    name = models.CharField('Название', max_length=1023)
    interface = models.ForeignKey(Interface, on_delete=models.DO_NOTHING, verbose_name='Интерфейс', null=True)
    type = models.CharField('Тип', max_length=8, choices=TypeChoices.choices, default=TypeChoices.INSIDER)
    bdu_id = models.CharField('Идентификатор БДУ', max_length=14, null=True)
    description = models.TextField('Описание', max_length=511, null=True)
    discovery_date = models.DateField('Дата выявления', null=True)
    cvss_v2 = models.CharField('CVSS 2.0', max_length=63, null=True)
    cvss_v3 = models.CharField('CVSS 3.0', max_length=63, null=True)
    cvss_v2_score = models.FloatField('CVSS 2.0 Оценка', null=True)
    cvss_v3_score = models.FloatField('CVSS 3.0 Оценка', null=True)
    severity = models.CharField('Критичность', max_length=255, null=True)
    bdu_countermeasure_advice = models.TextField('Возможный способ устранения', max_length=511, null=True)
    source_link = models.TextField('Ссылка на источник', max_length=3000, null=True)

    class Meta:
        verbose_name = 'Уязвимость'
        verbose_name_plural = 'Уязвимости'


class Threat(BaseModel):
    name = models.CharField('Название', max_length=1023)
    bdu_id = models.IntegerField('Идентификатор УБИ>', null=True)
    description = models.TextField('Описание', max_length=1023, null=True)
    asset_types = models.ManyToManyField(AssetType, verbose_name='Типы объектов')
    attackers = models.ManyToManyField(Attacker, verbose_name='Нарушители')
    confidentiality = models.BooleanField('Нарушает конфиденциальность', default=False)
    integrity = models.BooleanField('Нарушает целостность', default=False)
    availability = models.BooleanField('Нарушает доступность', default=False)

    #vulnerability = models.ForeignKey(Vulnerability, on_delete=models.DO_NOTHING, verbose_name='Уязвимость', null=True)

    class Meta:
        verbose_name = 'Угроза'
        verbose_name_plural = 'Угрозы'