# Generated by Django 4.2.9 on 2024-10-09 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0027_paymentmethod_salesinquiryspecies_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='salesinquiryspecies',
            options={'verbose_name_plural': 'Sales Inquiry Species'},
        ),
        migrations.AlterModelTable(
            name='salesinquiryspecies',
            table='sales_inquiry_species',
        ),
    ]