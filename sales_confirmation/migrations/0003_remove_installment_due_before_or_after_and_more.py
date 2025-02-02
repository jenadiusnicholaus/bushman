# Generated by Django 4.2.9 on 2024-10-24 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales_confirmation', '0002_installment_due_before_or_after'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='installment',
            name='due_before_or_after',
        ),
        migrations.AddField(
            model_name='installment',
            name='due_limit',
            field=models.CharField(choices=[('prior', 'Prior to Due Date'), ('after', 'After Due Date'), ('none', 'No Due Date')], default='none', max_length=255),
        ),
    ]
