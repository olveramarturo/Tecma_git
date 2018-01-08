# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-08 05:15
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TecmaMain', '0032_auto_20171204_1511'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recursosvideo',
            old_name='recursosvideo_archivo',
            new_name='recursosvideo_archivo_fx',
        ),
        migrations.AddField(
            model_name='recursosvideo',
            name='recursosvideo_archivo_qt',
            field=models.FileField(default='aa', upload_to='TecmaGeneral/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='metasreclutador',
            name='metas_fecha',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 12, 7, 22, 15, 17, 336055)),
        ),
    ]
