# Generated by Django 4.2.9 on 2024-10-08 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bm_hunting_settings', '0020_currency'),
        ('sales', '0007_alter_entityhuntinginfos_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactTyoe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Contact Types',
                'db_table': 'contact_types',
            },
        ),
        migrations.AddField(
            model_name='salespayment',
            name='currency',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sales_payment_currency_set', to='bm_hunting_settings.currency'),
        ),
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.CharField(max_length=100)),
                ('contact_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact_type_set', to='sales.contacttyoe')),
                ('entity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entity_contacts_set', to='sales.entity')),
            ],
            options={
                'verbose_name_plural': 'Contacts',
                'db_table': 'contacts',
            },
        ),
    ]