# Generated by Django 4.2.9 on 2024-10-24 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales_confirmation', '0003_remove_installment_due_before_or_after_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='installment',
            name='days',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
