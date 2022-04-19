from app.models.base_models import BaseModel
from django.db import models


class AssetType(BaseModel):
    name = models.CharField('Название', max_length=511)

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


class Interface(BaseModel):
    asset_type = models.ForeignKey(AssetType, on_delete=models.CASCADE, verbose_name='Тип объекта')

    class Meta:
        verbose_name = 'Интерфейс'
        verbose_name_plural = 'Интерфейсы'