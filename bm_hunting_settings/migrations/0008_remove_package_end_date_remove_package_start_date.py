# Generated by Django 5.0.4 on 2024-10-03 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bm_hunting_settings', '0007_remove_package_package_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='package',
            name='start_date',
        ),
    ]
