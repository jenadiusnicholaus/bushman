# Generated by Django 5.1.2 on 2024-12-30 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales_confirmation', '0064_accommodationcost_accommodationtype_address_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Address',
            new_name='AccommodationAddress',
        ),
    ]
