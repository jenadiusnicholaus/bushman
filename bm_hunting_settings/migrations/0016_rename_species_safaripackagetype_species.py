# Generated by Django 4.2.9 on 2024-10-08 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bm_hunting_settings', '0015_alter_blockhuntingspecieslimit_table'),
    ]

    operations = [
        migrations.RenameField(
            model_name='safaripackagetype',
            old_name='Species',
            new_name='species',
        ),
    ]