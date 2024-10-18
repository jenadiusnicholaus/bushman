# Generated by Django 5.0.4 on 2024-10-04 06:53

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hunter', '0018_clinetsalesorder'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientCustomizablePackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': 'Client Customizable Packages',
                'db_table': 'client_customizable_packages',
            },
        ),
        migrations.CreateModel(
            name='ClientSalesOrder',
            fields=[
                ('order_number', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name_plural': 'Sales Orders',
            },
        ),
        migrations.DeleteModel(
            name='ClinetSalesOrder',
        ),
    ]