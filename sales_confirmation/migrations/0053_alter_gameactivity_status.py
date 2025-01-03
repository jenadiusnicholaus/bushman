# Generated by Django 5.1.2 on 2024-12-08 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales_confirmation', '0052_gameactivity_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameactivity',
            name='status',
            field=models.CharField(blank=True, choices=[('CLOSED', 'Closed'), ('INITIATED', 'In Progress'), ('IN_PROGRESS', 'In Progress'), ('NOT_STARTED', 'Not Started')], default='NOT_STARTED', max_length=255, null=True),
        ),
    ]
