# Generated by Django 5.1.2 on 2024-11-13 14:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0015_alter_salesiquirypreference_no_of_companions_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entitycategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entity_category_set', to='sales.entitycategories'),
        ),
    ]
