# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-15 21:05
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TecmaMain', '0019_auto_20171112_0021'),
    ]

    operations = [
        migrations.CreateModel(
            name='Periodos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('periodo_nombre', models.CharField(blank=True, max_length=30)),
                ('periodo_inicio', models.DateField(blank=True, null=True)),
                ('periodo_fin', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='metasreclutador',
            name='metas_fecha',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 11, 15, 14, 5, 37, 215010)),
        ),
    ]