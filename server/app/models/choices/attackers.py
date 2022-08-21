from django.db import models


class AttackerPotentialChoices(models.TextChoices):
    """ ФСБ потенциал нарушителя """
    HIGH = 'HIGH', 'Высокий'
    MEDIUM = 'MEDIUM', 'Средний'
    LOW = 'LOW', 'Низкий'


class AttackerTypeChoices(models.TextChoices):
    INSIDER = 'INSIDER', 'Внутренний'
    OUTSIDER = 'OUTSIDER', 'Внешний'


class CapabilityLevelChoices(models.IntegerChoices):
    """ ФСТЭК уровень возможностей нарушителя """
    N4 = 4, 'Н4'
    N3 = 3, 'Н3'
    N2 = 2, 'Н2'
    N1 = 1, 'Н1'
