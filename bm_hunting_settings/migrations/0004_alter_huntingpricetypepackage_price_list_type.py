# Generated by Django 4.2.9 on 2024-10-24 19:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bm_hunting_settings', '0003_alter_huntingpricetypepackage_price_list_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='huntingpricetypepackage',
            name='price_list_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hunting_price_list_type_package', to='bm_hunting_settings.huntingpricelisttype'),
        ),
    ]
