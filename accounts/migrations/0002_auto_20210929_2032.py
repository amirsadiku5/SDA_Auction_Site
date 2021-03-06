# Generated by Django 3.2.7 on 2021-09-29 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='login',
            new_name='user',
        ),
        migrations.AlterField(
            model_name='account',
            name='account_status',
            field=models.CharField(choices=[('ACT', 'Active'), ('INA', 'Inactive'), ('BLC', 'Blocked')], default='INA', max_length=3),
        ),
        migrations.AlterField(
            model_name='account',
            name='account_type',
            field=models.CharField(choices=[('NRM', 'Normal Account'), ('PRM', 'Premium Account')], default='NRM', max_length=3),
        ),
    ]
