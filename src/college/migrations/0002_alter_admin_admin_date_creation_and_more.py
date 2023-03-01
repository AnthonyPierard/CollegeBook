# Generated by Django 4.1.6 on 2023-02-27 13:47

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('college', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='admin_date_creation',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 27, 14, 47, 48, 249581), verbose_name='Date de création du compte'),
        ),
        migrations.AlterField(
            model_name='evenement',
            name='admin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='evenement',
            name='even_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 27, 14, 47, 48, 249581), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='reserv_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 27, 14, 47, 48, 250578), verbose_name='Date de la réservation'),
        ),
    ]
