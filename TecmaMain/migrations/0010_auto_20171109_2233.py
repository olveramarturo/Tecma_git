# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-10 05:33
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TecmaMain', '0009_auto_20171109_2232'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reclutado',
            old_name='rec_proyecto',
            new_name='rec_proyecto_id',
        ),
        migrations.AlterField(
            model_name='metasreclutador',
            name='metas_fecha',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 11, 9, 22, 33, 33, 219986)),
        ),
    ]
