# Generated by Django 4.2.1 on 2024-10-03 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hunter', '0004_remove_hunter_passport_copy_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hunter',
            name='hunter_role',
            field=models.CharField(default='Main_Hunter', max_length=100),
        ),
        migrations.CreateModel(
            name='ProfessionHunter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profession', models.CharField(max_length=100)),
                ('hunter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profession_hunter', to='hunter.hunter')),
            ],
            options={
                'verbose_name_plural': 'Profession Hunters',
                'db_table': 'bm_profession_hunters',
            },
        ),
        migrations.CreateModel(
            name='CompanionHunter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('companion_name', models.CharField(max_length=100)),
                ('passport_number', models.CharField(max_length=100)),
                ('hunter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='companions', to='hunter.hunter')),
            ],
            options={
                'verbose_name_plural': 'Companions',
                'db_table': 'bm_companions',
            },
        ),
    ]
