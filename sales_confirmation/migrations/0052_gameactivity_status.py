# Generated by Django 5.1.2 on 2024-12-08 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales_confirmation', '0051_remove_salesconfirmationproposalpackage_hunting_license_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameactivity',
            name='status',
            field=models.CharField(blank=True, choices=[('CLOSED', 'Closed'), ('IN_PROGRESS', 'In Progress'), ('NOT_STARTED', 'Not Started')], default='NOT_STARTED', max_length=255, null=True),
        ),
    ]
