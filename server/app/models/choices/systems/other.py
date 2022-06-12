from django.db import models


class ISPDNTypeChoices(models.TextChoices):
    SPECIAL = 'SPECIAL', 'Cпециальные'
    BIOMETRIC = 'BIOMETRIC', 'Биометрические'
    PUBLIC = 'PUBLIC', 'Общедоступные'
    OTHER = 'OTHER', 'Иные'


class GISSizeChoices(models.TextChoices):
    REGIONAL = 'REGIONAL', 'Региональный'
    FEDERAL = 'FEDERAL', 'Федеральный'
    OBJECTED = 'OBJECTED', 'Объектовый'


class ProtectionLevelChoices(models.TextChoices):
    UZ1 = 'UZ1', 'УЗ1'
    UZ2 = 'UZ2', 'УЗ2'
    UZ3 = 'UZ3', 'УЗ3'
    UZ4 = 'UZ4', 'УЗ4'


class ProtectionClassChoices(models.TextChoices):
    K1 = 'K1', 'K1'
    K2 = 'K2', 'K2'
    K3 = 'K3', 'K3'


class SignificanceAttributeChoices(models.TextChoices):
    INSIGNIFICANT = 'INSIGNIFICANT', 'Незначимый'
    KZ1 = 'KZ1', 'KЗ1'
    KZ2 = 'KZ2', 'KЗ2'
    KZ3 = 'KZ3', 'KЗ3'


