# Generated by Django 5.1.2 on 2024-12-23 15:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bm_hunting_settings', '0024_unitofmeasurements'),
        ('requisition', '0012_alter_requestitemitems_unit_of_measurement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestitemitems',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bm_hunting_settings.currency'),
        ),
    ]
