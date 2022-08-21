from enum import Enum
from typing import Type, Callable

from django.db import models


def extend_choices(inherited_enum: Type[Enum]) -> Callable:
    def wrapper(added_enum: Type[Enum]) -> models.TextChoices:
        joined = {}
        for item in list(inherited_enum)+list(added_enum):
            joined[item.name] = item.value, item.label

        return models.TextChoices(added_enum.__name__, joined)
    return wrapper
