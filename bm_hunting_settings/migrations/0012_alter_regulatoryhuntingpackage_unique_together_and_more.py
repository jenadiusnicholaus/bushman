# Generated by Django 4.2.9 on 2024-10-28 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bm_hunting_settings', '0011_remove_huntingpackagecustomization_description'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='regulatoryhuntingpackage',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='regulatoryhuntingpackage',
            name='quota',
        ),
    ]