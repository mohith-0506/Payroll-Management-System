# Generated by Django 4.1 on 2024-11-18 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll_manager', '0003_alter_mpay_fin_year_alter_mpay_gross_dedn_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mpay',
            name='net_salary',
            field=models.IntegerField(default=198000),
        ),
    ]
