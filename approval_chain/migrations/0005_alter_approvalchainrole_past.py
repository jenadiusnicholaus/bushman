# Generated by Django 5.1.2 on 2024-12-16 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('approval_chain', '0004_alter_approvalchainlevels_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approvalchainrole',
            name='past',
            field=models.CharField(choices=[('APPROVED', 'APPROVED'), ('REJECTED', 'REJECTED')], default='APPROVED', max_length=255),
        ),
    ]