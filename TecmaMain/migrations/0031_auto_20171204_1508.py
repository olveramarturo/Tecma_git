# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-04 22:08
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TecmaMain', '0030_auto_20171204_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='metasreclutador',
            name='metas_requeridos_posicion_id',
            field=models.CharField(blank=True, max_length=4),
        ),
        migrations.AlterField(
            model_name='metasreclutador',
            name='metas_fecha',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 12, 4, 15, 8, 40, 12692)),
        ),
    ]
