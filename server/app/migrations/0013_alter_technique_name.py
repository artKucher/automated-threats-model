# Generated by Django 4.0.5 on 2022-06-12 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_technique_interface'),
    ]

    operations = [
        migrations.AlterField(
            model_name='technique',
            name='name',
            field=models.TextField(max_length=1024, verbose_name='Название'),
        ),
    ]
