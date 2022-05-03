from django.db import models

from app.models.choices.utils import extend_choices

GENERAL_VALUES = {

}

class BaseSpecificationChoices(models.TextChoices):
    FINANCIAL = 'FINANCIAL', 'Финансовая'
    HAS_PRIVATE_WEB_RESOURCES = 'HAS_PRIVATE_WEB_RESOURCES', 'Имеет частные WEB-ресурсы'
    HAS_PUBLIC_WEB_RESOURCES = 'HAS_PUBLIC_WEB_RESOURCES', 'Имеет публичные WEB-ресурсы'
    DEFENCE_SYSTEM = 'DEFENCE_SYSTEM', 'Оборонная система'
    SPECIAL_OR_BIOMETRIC_OFFICIALS_PERSONAL_DATA = (
        'SPECIAL_OR_BIOMETRIC_OFFICIALS_PERSONAL_DATA',
        'Обрабатывает специальные или биометрические данные госслужащих'
    )
    IMPACT_ON_PUBLIC_PERCEPTION = 'IMPACT_ON_PUBLIC_PERCEPTION', 'Влияние на общественное сознание'
    GOVERNMENT = 'GOVERNMENT', 'Государственная'
    BASIC = 'BASIC', 'Базовая'


@extend_choices(BaseSpecificationChoices)
class ISPDNSpecificationChoices(models.TextChoices):
    GOVERNMENT = 'GOVERNMENT', 'Государственная'


@extend_choices(BaseSpecificationChoices)
class GISSpecificationChoices(models.TextChoices): ...


@extend_choices(BaseSpecificationChoices)
class ASUTPSpecificationChoices(models.TextChoices):
    MANUFACTURE = 'MANUFACTURE', 'Производство'


@extend_choices(BaseSpecificationChoices)
class KIISpecificationChoices(models.TextChoices): ...