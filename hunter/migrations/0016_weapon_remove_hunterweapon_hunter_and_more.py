# Generated by Django 5.0.4 on 2024-10-03 18:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hunter', '0015_clienttype_remove_companionhunter_hunter_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weapon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weapon_type', models.CharField(max_length=100)),
                ('owner', models.CharField(max_length=100)),
                ('brand', models.CharField(max_length=100)),
                ('caliber', models.CharField(max_length=100)),
                ('serial_number', models.CharField(max_length=100)),
                ('ammo_quantity', models.IntegerField(default=0)),
                ('maker_number', models.CharField(max_length=100)),
                ('weapon_owner', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Hunter Weapons',
            },
        ),
        migrations.RemoveField(
            model_name='hunterweapon',
            name='hunter',
        ),
        migrations.RemoveField(
            model_name='huntinglicense',
            name='hunter',
        ),
        migrations.RenameField(
            model_name='clientpreferences',
            old_name='hunter',
            new_name='client',
        ),
        migrations.AlterModelTable(
            name='clientpreferences',
            table=None,
        ),
        migrations.AlterModelTable(
            name='hunteritinerary',
            table=None,
        ),
        migrations.CreateModel(
            name='ClientDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(choices=[('Passport_Copy', 'Travel Packet(Passport Copy)'), ('Passport_Photo', 'Travel Packet(Passport  Photo'), ('Visa', 'Visa'), ('Gun Permits', 'Gun Permits'), ('CITES Documentation', 'CITES Documentation')], max_length=100)),
                ('document', models.FileField(upload_to='documents/')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hunder_documents', to='hunter.client')),
            ],
            options={
                'verbose_name_plural': 'Hunter Documents',
            },
        ),
        migrations.CreateModel(
            name='HuntingClientLicense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_number', models.CharField(max_length=100)),
                ('issue_date', models.DateField()),
                ('expiry_date', models.DateField()),
                ('licence_document', models.FileField(upload_to='documents/')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hunting_license', to='hunter.client')),
            ],
            options={
                'verbose_name_plural': 'Hunting Licenses',
            },
        ),
        migrations.DeleteModel(
            name='HunterDocument',
        ),
        migrations.DeleteModel(
            name='HunterWeapon',
        ),
        migrations.DeleteModel(
            name='HuntingLicense',
        ),
    ]