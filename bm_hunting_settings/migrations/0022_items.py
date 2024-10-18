# Generated by Django 4.2.9 on 2024-10-08 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bm_hunting_settings', '0021_identitytype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('count', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name_plural': 'Items',
                'db_table': 'items',
            },
        ),
    ]