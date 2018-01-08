# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-26 00:20
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TecmaMain', '0021_auto_20171125_1719'),
    ]

    operations = [
        migrations.CreateModel(
            name='Planta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('planta_nombre', models.CharField(blank=True, max_length=30)),
                ('planta_calle', models.CharField(blank=True, max_length=30)),
                ('planta_numero', models.CharField(blank=True, max_length=10)),
            ],
        ),
        migrations.AlterField(
            model_name='metasreclutador',
            name='metas_fecha',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 11, 25, 17, 20, 42, 841800)),
        ),
    ]