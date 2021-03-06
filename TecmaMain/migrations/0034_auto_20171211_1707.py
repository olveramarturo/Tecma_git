# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-12 00:07
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TecmaMain', '0033_auto_20171207_2215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metasreclutador',
            name='metas_fecha',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 12, 11, 17, 7, 58, 487765)),
        ),
        migrations.AlterField(
            model_name='metasreclutador',
            name='metas_requeridos_posicion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TecmaMain.Puesto'),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='proyecto_video',
            field=models.FileField(blank=True, upload_to='TecmaGeneral/'),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='proyecto_video_tecma',
            field=models.FileField(blank=True, upload_to='TecmaGeneral/'),
        ),
    ]
