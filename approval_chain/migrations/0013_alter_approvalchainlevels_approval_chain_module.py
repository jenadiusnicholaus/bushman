# Generated by Django 5.1.2 on 2024-12-17 09:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('approval_chain', '0012_alter_approvalchain_approval_chain_module'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approvalchainlevels',
            name='approval_chain_module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='levels', to='approval_chain.approvalchainmodule'),
        ),
    ]