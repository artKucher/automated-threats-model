# Generated by Django 4.0.5 on 2022-06-13 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_alter_gisclass_specification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asutpclass',
            name='specification',
            field=models.CharField(choices=[('FINANCIAL', 'Финансовая'), ('HAS_PRIVATE_WEB_RESOURCES', 'Имеет частные WEB-ресурсы'), ('HAS_PUBLIC_WEB_RESOURCES', 'Имеет публичные WEB-ресурсы'), ('DEFENCE_SYSTEM', 'Оборонная система'), ('SPECIAL_OR_BIOMETRIC_OFFICIALS_PERSONAL_DATA', 'Обрабатывает специальные или биометрические данные госслужащих'), ('IMPACT_ON_PUBLIC_PERCEPTION', 'Влияние на общественное сознание'), ('BASIC', 'Базовая'), ('GOVERNMENT', 'Государственная'), ('INDUSTRY', 'Промышленность')], max_length=44, verbose_name='Спецификация'),
        ),
    ]
