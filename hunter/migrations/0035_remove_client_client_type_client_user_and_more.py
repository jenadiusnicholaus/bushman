# Generated by Django 5.0.4 on 2024-10-04 09:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_remove_userprofile_passport_number'),
        ('hunter', '0034_companion_observer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='client_type',
        ),
        migrations.AddField(
            model_name='client',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='main_client', to='authentication.userprofile'),
        ),
        migrations.DeleteModel(
            name='ClientType',
        ),
    ]
