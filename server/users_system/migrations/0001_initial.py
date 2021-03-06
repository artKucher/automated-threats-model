# Generated by Django 4.0.4 on 2022-04-27 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('assets', models.ManyToManyField(to='app.asset', verbose_name='Объекты')),
                ('asutp_classes', models.ManyToManyField(to='app.asutpclass', verbose_name='Классы АСУТП')),
                ('gis_classes', models.ManyToManyField(to='app.gisclass', verbose_name='Классы ГИС')),
                ('ispdn_classes', models.ManyToManyField(to='app.ispdnclass', verbose_name='Классы ИСПДн')),
                ('kii_classes', models.ManyToManyField(to='app.kiiclass', verbose_name='Классы КИИ')),
            ],
            options={
                'verbose_name': 'Система',
                'verbose_name_plural': 'Системы',
            },
        ),
    ]
