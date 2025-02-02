# Generated by Django 5.1.2 on 2024-12-19 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bm_hunting_settings', '0021_salespackages_regulatory_package'),
    ]

    operations = [
        migrations.AlterField(
            model_name='huntingtype',
            name='name',
            field=models.CharField(choices=[('1x1', '1x1'), ('2x1', '2x1'), ('2x2', '2x2'), ('3x1', '3x1'), ('3x2', '3x2'), ('4x1', '4x1'), ('4x2', '4x2'), ('5x2', '5x2'), ('5x1', '5x1'), ('6x1', '6x1'), ('7x1', '7x1'), ('8x1', '8x1'), ('9x1', '9x1'), ('10x1', '10x1')], max_length=100, unique=True),
        ),
    ]
