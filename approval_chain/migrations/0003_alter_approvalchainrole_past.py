# Generated by Django 5.1.2 on 2024-12-16 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('approval_chain', '0002_alter_approvalchainlevels_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approvalchainrole',
            name='past',
            field=models.BooleanField(choices=[('APPROVED', 'APPROVED'), ('REJECTED', 'REJECTED')], default='APPROVED'),
        ),
    ]
