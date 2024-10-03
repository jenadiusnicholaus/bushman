# Generated by Django 5.0.4 on 2024-10-03 15:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bm_hunting_settings', '0005_alter_blockhuntingspecieslimit_table'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PackageType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Package Types',
                'db_table': 'package_types',
            },
        ),
        migrations.CreateModel(
            name='TrophyFees',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Trophy Fees',
                'db_table': 'trophy_fees',
            },
        ),
        migrations.CreateModel(
            name='SalesPackageHuntingSpecies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('limit', models.IntegerField(default=0)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hunting_species', to='bm_hunting_settings.species')),
            ],
            options={
                'verbose_name_plural': 'Hunting Species',
                'db_table': 'package_hunting_species',
            },
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_name', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('number_of_safari_spots', models.IntegerField(default=0)),
                ('number_of_hunters', models.IntegerField(default=0)),
                ('upgrade_fees', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('number_of_days', models.IntegerField(default=0)),
                ('companion_hunter_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('observer_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('change_of_area_fees', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('baiting_vehicle_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('firearm_hire_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('wifi_charges', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('total_cost', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10)),
                ('is_active', models.BooleanField(default=True)),
                ('status', models.CharField(choices=[('Draft', 'Draft'), ('Published', 'Published')], default='Draft', max_length=100)),
                ('professional_hunter_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to=settings.AUTH_USER_MODEL)),
                ('hunting_block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hunting_block', to='bm_hunting_settings.huntingblock')),
                ('hunting_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hunting_type', to='bm_hunting_settings.huntingtype')),
                ('package_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='package_type', to='bm_hunting_settings.packagetype')),
                ('hunting_species', models.ManyToManyField(related_name='hunting_species', to='bm_hunting_settings.salespackagehuntingspecies')),
                ('trophy_fees_list', models.ManyToManyField(related_name='trophy_fees_list', to='bm_hunting_settings.trophyfees')),
            ],
            options={
                'verbose_name_plural': 'Pre-defined Sales Packages',
                'db_table': 'pre_defined_sales_packages',
            },
        ),
    ]
