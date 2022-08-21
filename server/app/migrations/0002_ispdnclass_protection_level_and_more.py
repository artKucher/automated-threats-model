# Generated by Django 4.0.4 on 2022-04-27 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ispdnclass',
            name='protection_level',
            field=models.CharField(choices=[('UZ1', 'УЗ1'), ('UZ2', 'УЗ2'), ('UZ3', 'УЗ3'), ('UZ4', 'УЗ4')], default='UZ1', max_length=3, verbose_name='Уровень защищенности'),
        ),
        migrations.AddField(
            model_name='kiiclass',
            name='significance_attribute',
            field=models.CharField(choices=[('KZ1', 'KЗ1'), ('KZ2', 'KЗ2'), ('KZ3', 'KЗ3')], default='KZ1', max_length=3, verbose_name='Критерий значимости'),
        ),
    ]