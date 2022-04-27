from django.db import models


class AttackerPotentialChoices(models.TextChoices):
    """ ФСБ потенциал нарушителя """
    HIGH = 'HIGH', 'Высокий'
    MEDIUM = 'MEDIUM', 'Средний'
    LOW = 'LOW', 'Низкий'


class AttackerTypeChoices(models.TextChoices):
    INSIDER = 'INSIDER', 'Внутренний'
    OUTSIDER = 'OUTSIDER', 'Внешний'


class CapabilityLevelChoices(models.TextChoices):
    """ ФСТЭК уровень возможностей нарушителя """
    N4 = 'N4', 'Н4'
    N3 = 'N3', 'Н3'
    N2 = 'N2', 'Н2'
    N1 = 'N1', 'Н1'