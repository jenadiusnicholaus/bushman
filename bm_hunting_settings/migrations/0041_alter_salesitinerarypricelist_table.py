# Generated by Django 5.1.2 on 2024-12-31 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bm_hunting_settings', '0040_rename_salescharterspricelist_salesitinerarypricelist'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='salesitinerarypricelist',
            table='sales_charters_price_list',
        ),
    ]
