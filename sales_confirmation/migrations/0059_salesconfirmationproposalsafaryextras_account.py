# Generated by Django 5.1.2 on 2024-12-28 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales_confirmation', '0058_alter_salesconfirmationproposalsafaryextras_safary_extras_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesconfirmationproposalsafaryextras',
            name='account',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]