# Generated by Django 5.1.2 on 2024-12-17 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('approval_chain', '0007_alter_approvalchainmodule_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='approvalchainlevels',
            name='leve_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
