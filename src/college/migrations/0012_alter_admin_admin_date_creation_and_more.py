# Generated by Django 4.1.7 on 2023-02-21 15:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('college', '0011_alter_admin_admin_date_creation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='admin_date_creation',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 21, 16, 3, 26, 114102), verbose_name='Date de création du compte'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='reserv_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 21, 16, 3, 26, 114102), verbose_name='Date de la réservation'),
        ),
    ]