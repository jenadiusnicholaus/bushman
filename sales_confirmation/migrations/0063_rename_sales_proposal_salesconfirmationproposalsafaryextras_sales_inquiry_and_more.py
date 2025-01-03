# Generated by Django 5.1.2 on 2024-12-29 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bm_hunting_settings', '0035_safaryextras_charges_per'),
        ('sales', '0023_alter_salesinquiry_season'),
        ('sales_confirmation', '0062_alter_salesconfirmationproposalsafaryextras_sales_proposal'),
    ]

    operations = [
        migrations.RenameField(
            model_name='salesconfirmationproposalsafaryextras',
            old_name='sales_proposal',
            new_name='sales_inquiry',
        ),
        migrations.AlterUniqueTogether(
            name='salesconfirmationproposalsafaryextras',
            unique_together={('safari_extras', 'sales_inquiry')},
        ),
    ]
