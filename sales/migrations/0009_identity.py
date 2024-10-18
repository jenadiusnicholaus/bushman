# Generated by Django 4.2.9 on 2024-10-08 10:21

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bm_hunting_settings', '0021_identitytype'),
        ('sales', '0008_contacttyoe_salespayment_currency_contacts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Identity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identity_number', models.CharField(max_length=100)),
                ('create_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('entity_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='identity', to='sales.entity')),
                ('identity_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='identity_type', to='bm_hunting_settings.identitytype')),
            ],
            options={
                'verbose_name_plural': 'Identities',
                'db_table': 'identities',
            },
        ),
    ]