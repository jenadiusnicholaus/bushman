# Generated by Django 5.1.2 on 2024-12-27 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bm_hunting_settings', '0025_alter_huntingpackagecompanionshunter_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='species',
            name='type',
            field=models.CharField(blank=True, choices=[('MAIN', 'Main Species'), ('NORMAL', 'Normal Species')], max_length=100, null=True),
        ),
    ]
