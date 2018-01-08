# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-10 05:03
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ciudades',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ciudad', models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Comunicacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('como_se_entero', models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Estados',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='MetasReclutador',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metas_fecha', models.DateField(blank=True, default=datetime.datetime(2017, 11, 9, 22, 3, 25, 419153))),
                ('metas_requeridos', models.CharField(blank=True, max_length=20)),
                ('metas_requeridos_posicion', models.CharField(blank=True, max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Metas',
            },
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supervisor', models.CharField(blank=True, max_length=10)),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Perfiles',
            },
        ),
        migrations.CreateModel(
            name='Prestaciones',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prestaciones_nombre', models.CharField(blank=True, max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Prestaciones',
            },
        ),
        migrations.CreateModel(
            name='ProcesoRH',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('procesorh_llego', models.CharField(max_length=2)),
                ('procesorh_cambiocita', models.DateField(blank=True, null=True)),
                ('procesorh_entrevista', models.CharField(max_length=2)),
                ('procesorh_contratado', models.CharField(max_length=2)),
                ('procesorh_rechazo', models.CharField(blank=True, max_length=50)),
                ('procesorh_notas', models.CharField(blank=True, max_length=250)),
                ('procesorh_folio', models.DateField(blank=True, default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proyecto_nombre', models.CharField(blank=True, max_length=30)),
                ('proyecto_descripcion', models.CharField(blank=True, max_length=120)),
                ('proyecto_ubicacion', models.CharField(blank=True, max_length=30)),
                ('proyecto_video', models.FileField(blank=True, upload_to='vidTecma_General')),
                ('proyecto_video_tecma', models.FileField(blank=True, upload_to='vidTecmaPro')),
                ('proyecto_url', models.CharField(blank=True, max_length=30)),
                ('proyecto_img', models.ImageField(upload_to='imagenesTecma')),
            ],
        ),
        migrations.CreateModel(
            name='Puesto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puesto_nombre', models.CharField(blank=True, max_length=20)),
                ('puesto_proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TecmaMain.Proyecto')),
            ],
        ),
        migrations.CreateModel(
            name='PuntoReclutamiento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('punto_reclutamiento', models.CharField(blank=True, max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Puntos de Reclutamiento',
            },
        ),
        migrations.CreateModel(
            name='RazonRechazo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razonrechazo', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Reclutado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rec_nombres', models.CharField(blank=True, max_length=40)),
                ('rec_apellido_paterno', models.CharField(blank=True, max_length=30)),
                ('rec_apellido_materno', models.CharField(blank=True, max_length=30)),
                ('rec_fecha_nacimiento', models.DateField(blank=True)),
                ('rec_email', models.CharField(blank=True, max_length=30)),
                ('rec_telefono', models.CharField(blank=True, max_length=30)),
                ('rec_calle', models.CharField(blank=True, max_length=30)),
                ('rec_numero', models.CharField(blank=True, max_length=30)),
                ('rec_ciudad', models.CharField(blank=True, max_length=30)),
                ('rec_estado', models.CharField(blank=True, max_length=30)),
                ('rec_codigo_postal', models.CharField(blank=True, max_length=30)),
                ('rec_fecha_entrevista', models.DateField(blank=True)),
                ('rec_fecha_captacion', models.DateField(blank=True, default=datetime.datetime.now)),
                ('rec_reclutador', models.CharField(blank=True, max_length=30)),
                ('rec_proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TecmaMain.Proyecto')),
                ('rec_proyecto_puesto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TecmaMain.Puesto')),
            ],
        ),
        migrations.CreateModel(
            name='RecursosVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recursosvideo_nombre', models.CharField(choices=[('videoTecmaMain', 'Video Mi nueva casa'), ('videoTecmaEvent', 'Video Mi familia Tecma')], max_length=40)),
                ('recursosvideo_descripcion', models.CharField(max_length=50)),
                ('recursosvideo_url', models.URLField(blank=True)),
                ('recursosvideo_archivo', models.FileField(upload_to='TecmaGeneral/')),
            ],
        ),
        migrations.CreateModel(
            name='ReporteContacto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_registro', models.DateField(blank=True, null=True)),
                ('reclutador', models.CharField(blank=True, max_length=30)),
                ('como_se_entero', models.CharField(blank=True, max_length=30)),
                ('punto_reclutamiento', models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Sueldos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sueldos_salario_diario', models.CharField(blank=True, max_length=10)),
                ('sueldos_bonos', models.CharField(blank=True, max_length=10)),
                ('sueldos_proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TecmaMain.Proyecto')),
                ('sueldos_puesto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TecmaMain.Puesto')),
            ],
            options={
                'verbose_name_plural': 'Sueldos',
            },
        ),
        migrations.AddField(
            model_name='procesorh',
            name='procesorh_reclutado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TecmaMain.Reclutado'),
        ),
        migrations.AddField(
            model_name='prestaciones',
            name='prestaciones_proyecto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TecmaMain.Proyecto'),
        ),
        migrations.AddField(
            model_name='metasreclutador',
            name='metas_proyecto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TecmaMain.Proyecto'),
        ),
        migrations.AddField(
            model_name='metasreclutador',
            name='metas_reclutador',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ciudades',
            name='estado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TecmaMain.Estados'),
        ),
    ]
