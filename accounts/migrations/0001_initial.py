# Generated by Django 3.2.7 on 2021-09-28 18:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=128)),
                ('address', models.CharField(max_length=128)),
                ('account_creation_date', models.DateField(auto_now_add=True)),
                ('account_status', models.CharField(choices=[('ACT', 'Active'), ('INA', 'Inactive'), ('BLC', 'User')], default='INA', max_length=3)),
                ('account_type', models.CharField(choices=[('ACT', 'Active'), ('INA', 'Inactive'), ('BLC', 'User')], default='NRM', max_length=3)),
                ('avatar', models.ImageField(upload_to='images/')),
                ('login', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]