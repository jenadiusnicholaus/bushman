# Generated by Django 5.1.2 on 2024-12-31 07:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bm_hunting_settings', '0039_rename_salesitinerarypricelist_salescharterspricelist'),
        ('sales_confirmation', '0072_salesconfirmationcharterspricelist'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SalesChartersPriceList',
            new_name='SalesItineraryPriceList',
        ),
    ]
