# Generated by Django 5.1.2 on 2024-12-30 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales_confirmation', '0068_alter_accommodationcost_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accommodationcost',
            old_name='cost',
            new_name='amount',
        ),
    ]