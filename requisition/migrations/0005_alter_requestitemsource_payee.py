# Generated by Django 5.1.2 on 2024-12-17 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requisition', '0004_alter_requestitemaccount_descriptions_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestitemsource',
            name='payee',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
