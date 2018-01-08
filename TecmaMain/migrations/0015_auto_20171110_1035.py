# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-10 17:35
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TecmaMain', '0014_auto_20171110_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metasreclutador',
            name='metas_fecha',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 11, 10, 10, 35, 1, 897712)),
        ),
        migrations.AlterField(
            model_name='reclutado',
            name='rec_proyecto',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='reclutado',
            name='rec_proyecto_puesto',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
