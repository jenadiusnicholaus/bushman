# Generated by Django 5.1.2 on 2024-12-16 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('approval_chain', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approvalchainlevels',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')], max_length=255),
        ),
    ]
