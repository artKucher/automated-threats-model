# Generated by Django 4.0.5 on 2022-06-08 04:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_technique_capability_technique_interface_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interface',
            name='asset_type',
        ),
        migrations.AddField(
            model_name='assettype',
            name='interfaces',
            field=models.ManyToManyField(to='app.interface', verbose_name='Интерфейсы'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='asset_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assets', to='app.assettype', verbose_name='Тип объекта'),
        ),
        migrations.AlterField(
            model_name='attacker',
            name='capability',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attackers', to='app.capability', verbose_name='Возможности'),
        ),
        migrations.AlterField(
            model_name='capability',
            name='level',
            field=models.IntegerField(choices=[(4, 'Н4'), (3, 'Н3'), (2, 'Н2'), (1, 'Н1')], null=True, verbose_name='Уровень'),
        ),
        migrations.AlterField(
            model_name='threatsimplementationmethod',
            name='threats',
            field=models.ManyToManyField(related_name='implementation_methods', to='app.threat', verbose_name='Угрозы'),
        ),
    ]
