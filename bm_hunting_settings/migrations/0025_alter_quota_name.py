# Generated by Django 4.2.9 on 2024-10-08 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bm_hunting_settings', '0024_alter_packagetype_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quota',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]