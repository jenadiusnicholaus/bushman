# Generated by Django 5.1.2 on 2024-11-14 06:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0016_alter_entitycategory_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entitycategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entity_category', to='sales.entitycategories'),
        ),
    ]
