# Generated by Django 5.1.2 on 2024-11-11 09:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales_confirmation', '0019_alter_salesquotaspeciesstatus_quota'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesConfirmationContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_number', models.CharField(blank=True, max_length=255, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('contract_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('sales_confirmation_proposal', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='contract', to='sales_confirmation.salesconfirmationproposal')),
            ],
            options={
                'verbose_name_plural': 'Sales Confirmation Contracts',
                'db_table': 'sales_confirmation_contract',
            },
        ),
    ]
