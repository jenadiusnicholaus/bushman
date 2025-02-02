# Generated by Django 4.2.9 on 2024-10-23 20:03

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bm_hunting_settings', '0001_initial'),
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesConfirmationProposal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirmation_date', models.DateField(auto_now=True, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('client', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sales_confirmation_proposal_client', to='sales.entity')),
                ('sales_inquiry', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sales_confirmation_proposal', to='sales.salesinquiry')),
            ],
            options={
                'verbose_name_plural': 'Sales Confirmation Proposals',
                'db_table': 'sales_confirmation_proposal',
                'unique_together': {('sales_inquiry', 'id')},
            },
        ),
        migrations.CreateModel(
            name='SalesConfirmationProposalPackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hunting_license', models.CharField(blank=True, max_length=255, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('package', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sales_confirmation_package_package', to='bm_hunting_settings.salespackages')),
                ('sales_confirmation_proposal', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sales_confirmation_package', to='sales_confirmation.salesconfirmationproposal')),
            ],
            options={
                'verbose_name_plural': 'Sales Confirmation Packages',
                'db_table': 'sales_confirmation_package',
            },
        ),
        migrations.CreateModel(
            name='SalesConfirmationProposalItinerary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('airport_name', models.CharField(blank=True, max_length=255, null=True, validators=[django.core.validators.MaxLengthValidator(255)])),
                ('arrival', models.DateTimeField(blank=True, null=True)),
                ('charter_in', models.DateTimeField(blank=True, null=True)),
                ('charter_out', models.DateTimeField(blank=True, null=True)),
                ('hotel_booking', models.CharField(blank=True, max_length=255, null=True, validators=[django.core.validators.MaxLengthValidator(255)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sales_confirmation_proposal', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='itineraries', to='sales_confirmation.salesconfirmationproposal')),
            ],
            options={
                'verbose_name_plural': 'Sales Confirmation Itineraries',
                'db_table': 'sales_confirmation_itinerary',
            },
        ),
        migrations.CreateModel(
            name='SalesConfirmationProposalClientPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preference_name', models.CharField(blank=True, max_length=255, null=True, validators=[django.core.validators.MaxLengthValidator(255)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sales_confirmation_proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_preferences', to='sales_confirmation.salesconfirmationproposal')),
            ],
            options={
                'verbose_name_plural': 'Sales Confirmation Client Preferences',
                'db_table': 'sales_confirmation_client_preference',
            },
        ),
        migrations.CreateModel(
            name='SalesConfirmationProposalAdditionalService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.CharField(blank=True, max_length=255, null=True, validators=[django.core.validators.MaxLengthValidator(255)])),
                ('quantity', models.IntegerField(blank=True, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sales_confirmation_proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='additional_services', to='sales_confirmation.salesconfirmationproposal')),
            ],
            options={
                'verbose_name_plural': 'Sales Confirmation Additional Services',
                'db_table': 'sales_confirmation_additional_service',
            },
        ),
        migrations.CreateModel(
            name='Installment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('amount_due', models.DecimalField(decimal_places=2, max_digits=10)),
                ('due_date', models.DateField()),
                ('sales_confirmation_proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='installments', to='sales_confirmation.salesconfirmationproposal')),
            ],
            options={
                'verbose_name_plural': 'Installments',
                'db_table': 'sales_confirmation_installment',
            },
        ),
    ]
