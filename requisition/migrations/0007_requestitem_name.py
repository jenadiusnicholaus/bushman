# Generated by Django 5.1.2 on 2024-12-17 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requisition', '0006_alter_requestitemaccount_exchange_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestitem',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
