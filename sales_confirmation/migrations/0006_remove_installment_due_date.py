# Generated by Django 4.2.9 on 2024-10-24 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales_confirmation', '0005_alter_installment_due_limit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='installment',
            name='due_date',
        ),
    ]
