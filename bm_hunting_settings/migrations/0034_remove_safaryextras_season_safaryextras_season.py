# Generated by Django 5.1.2 on 2024-12-28 15:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bm_hunting_settings', '0033_rename_seasons_safaryextras_season'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='safaryextras',
            name='season',
        ),
        migrations.AddField(
            model_name='safaryextras',
            name='season',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='safary_extras_season_set', to='bm_hunting_settings.seasons'),
        ),
    ]