# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-10 05:08
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TecmaMain', '0002_auto_20171109_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metasreclutador',
            name='metas_fecha',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 11, 9, 22, 8, 35, 349316)),
        ),
    ]
