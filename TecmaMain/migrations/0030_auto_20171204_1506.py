# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-04 22:06
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TecmaMain', '0029_auto_20171201_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metasreclutador',
            name='metas_fecha',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 12, 4, 15, 6, 58, 362180)),
        ),
    ]
