# Generated by Django 5.1.2 on 2024-12-28 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bm_hunting_settings', '0034_remove_safaryextras_season_safaryextras_season'),
    ]

    operations = [
        migrations.AddField(
            model_name='safaryextras',
            name='charges_per',
            field=models.CharField(blank=True, choices=[('PER_HOUR', 'Per Hour'), ('PER_DAY', 'Per Day'), ('PER_PERSON', 'Per Person'), ('PER_ROUND', 'Per Round')], max_length=255, null=True),
        ),
    ]
