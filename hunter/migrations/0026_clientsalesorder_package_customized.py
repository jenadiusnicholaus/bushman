# Generated by Django 5.0.4 on 2024-10-04 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hunter', '0025_clientsalesorder_pre_def_package'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientsalesorder',
            name='package_customized',
            field=models.BooleanField(default=False),
        ),
    ]
