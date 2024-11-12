# Generated by Django 5.1.2 on 2024-11-11 09:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bm_hunting_settings', '0017_alter_huntingpackagecompanionshunter_days_and_more'),
        ('sales_confirmation', '0022_salesconfirmationcontract_enity_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enitycontactdates',
            name='amended_id',
        ),
        migrations.RemoveField(
            model_name='enitycontractpermit',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='enitycontractpermit',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='enitycontactdates',
            name='amendment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='amendments', to='sales_confirmation.enitycontactdates'),
        ),
        migrations.CreateModel(
            name='GameActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('entity_contract_permit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_activity_set', to='sales_confirmation.enitycontractpermit')),
            ],
            options={
                'verbose_name_plural': 'Game Activities',
                'db_table': 'game_activity',
            },
        ),
        migrations.CreateModel(
            name='GameKilledActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('spacies_gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female')], max_length=255, null=True)),
                ('status', models.CharField(blank=True, choices=[('KILLED', 'Killed'), ('WONDERED', 'Wondered')], max_length=255, null=True)),
                ('game_killed_registration', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_killed_activity_set', to='sales_confirmation.gameactivity')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='game_killed_activity_location_set', to='bm_hunting_settings.locations')),
                ('species', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_killed_activity_species_set', to='bm_hunting_settings.species')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='game_killed_activity_Created_by_user_set', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Game Killed Activities',
                'db_table': 'game_killed_activity',
            },
        ),
    ]