# Generated by Django 4.2.9 on 2024-10-08 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hunter', '0047_remove_entitycategory_category_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ClientDocument',
            new_name='Document',
        ),
    ]