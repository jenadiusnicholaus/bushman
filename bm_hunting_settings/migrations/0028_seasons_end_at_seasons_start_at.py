# Generated by Django 5.1.2 on 2024-12-27 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bm_hunting_settings', '0027_alter_species_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='seasons',
            name='end_at',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='seasons',
            name='start_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]