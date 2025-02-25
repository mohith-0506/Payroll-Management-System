# Generated by Django 4.1 on 2024-11-18 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll_manager', '0002_mpay_achivement_reward'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mpay',
            name='fin_year',
            field=models.IntegerField(default=2024),
        ),
        migrations.AlterField(
            model_name='mpay',
            name='gross_dedn',
            field=models.IntegerField(default=2000),
        ),
        migrations.AlterField(
            model_name='mpay',
            name='gross_salary',
            field=models.IntegerField(default=200000),
        ),
        migrations.AlterField(
            model_name='mpay',
            name='net_salary',
            field=models.IntegerField(verbose_name=198000),
        ),
    ]
