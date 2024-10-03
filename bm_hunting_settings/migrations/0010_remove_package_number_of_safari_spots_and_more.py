# Generated by Django 5.0.4 on 2024-10-03 19:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bm_hunting_settings', '0009_companionhuntercost_safaripackagetype_species_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='number_of_safari_spots',
        ),
        migrations.CreateModel(
            name='SpeciesAvailabilityAndCost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('availability', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('hunting_block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='species_availability_and_cost', to='bm_hunting_settings.huntingblock')),
                ('species', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='species_availability_and_cost', to='bm_hunting_settings.species')),
            ],
            options={
                'verbose_name_plural': 'Species Availability and Cost',
                'db_table': 'package_species_availability_and_cost',
            },
        ),
    ]
