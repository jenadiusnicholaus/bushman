# Generated by Django 5.1.2 on 2024-12-17 13:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('approval_chain', '0014_alter_approvalchainlevels_level_number'),
        ('requisition', '0009_remarkshistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requisition',
            name='approval_chain_module',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='requisition_module', to='approval_chain.approvalchainmodule'),
        ),
    ]