from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime


# Create your models here.

#------------------------------------------------------------------------------
# Seccion Reclutador modelos relacionados con el perfil reclutador
#------------------------------------------------------------------------------

class Periodos(models.Model):
    ''' Tabla con referencias de los periodos
        o ciclos de trabajo para los reclutadores
    '''
    periodo_nombre = models.CharField(max_length=30, blank=True)
    periodo_inicio = models.DateField(null=True, blank=True)
    periodo_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        ''''''
        nombre = self.periodo_nombre
        inicio = self.periodo_inicio
        identificador = ("%s - Inicio: %s" % (nombre, inicio))
        return identificador


class Estados(models.Model):
    '''Modelo de referencia para estados'''
    estado = models.CharField(max_length=30, blank=True)

    def __str__(self):
        ''''''
        return self.estado


class Ciudades(models.Model):
    '''Modelo de referencia para Ciudades'''
    estado = models.ForeignKey(Estados)
    ciudad = models.CharField(max_length=30, blank=True)

    def __str__(self):
        ''''''
        locacion = '%s, %s' % (self.ciudad, self.estado)
        return locacion


class Planta(models.Model):
    ''' Modelo de referencia para las plantas '''
    planta_nombre = models.CharField(max_length=30, blank=True)
    planta_calle = models.CharField(max_length=30, blank=True)
    planta_numero = models.CharField(max_length=10, blank=True)

    def __str__(self):
        ''''''
        return self.planta_nombre


class RazonRechazo(models.Model):
    '''Lista de opciones para el selector de rechazo, se editan en admin'''
    razonrechazo = models.CharField(max_length=50, blank=True)

    def __str(self):
        ''''''
        rr = self.razonrechazo
        return rr


class ReporteContacto(models.Model):
    ''''''
    fecha_registro = models.DateField(null=True, blank=True)
    reclutador = models.CharField(max_length=30, blank=True)
    como_se_entero = models.CharField(max_length=30, blank=True)
    punto_reclutamiento = models.CharField(max_length=30, blank=True)

    def __init__(self):
        ''' Metodo default '''
        super(ReporteContacto, self).__init__()


class Perfil(models.Model):
    ''' Extending the User model '''
    class Meta:
        '''Corregir plurales'''
        verbose_name_plural = 'Perfiles'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    supervisor = models.CharField(max_length=10, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    planta_asignado = models.ForeignKey(Planta)

    def __str__(self):
        '''Regresar el id del ususario'''
        return str(self.user)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        '''Una instancia de ususario se ha generado'''
        if created:
            Perfil.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        '''Se extienden el metodo save para los dos modelos'''
        instance.perfil.save()


class Proyecto(models.Model):
    '''Modelo con la informacion de cada proyecto'''
    proyecto_nombre = models.CharField(max_length=30, blank=True)
    proyecto_descripcion = models.CharField(max_length=120, blank=True)
    proyecto_ubicacion = models.CharField(max_length=30, blank=True)
    # Video de presentacion de cada proyecto
    proyecto_video = models.FileField(upload_to='TecmaGeneral/', blank=True)
    # Video de eventos de Tecma
    proyecto_video_tecma = models.FileField(
        upload_to='TecmaGeneral/', blank=True)
    proyecto_img = models.ImageField(upload_to='imagenesTecma')
    proyecto_planta = models.ForeignKey(Planta)

    def __str__(self):
        '''Regresar nombre'''
        return self.proyecto_nombre


class Puesto(models.Model):
    '''Lista de puestos por proyecto'''
    puesto_proyecto = models.ForeignKey(Proyecto)
    puesto_nombre = models.CharField(max_length=20, blank=True)

    def __str__(self):
        '''Regresar el nombre'''
        pjid = self.puesto_nombre + ' - ' + str(self.puesto_proyecto)
        return pjid


class MetasReclutador(models.Model):
    '''Almacenamiento de las metas del reclutador - muchos a uno '''
    class Meta:
        '''Corregir plurales'''
        verbose_name_plural = 'Metas'

    metas_reclutador = models.ForeignKey(User)
    metas_fecha = models.DateField(default=datetime.now(), blank=True)
    metas_proyecto = models.ForeignKey(Proyecto)
    metas_requeridos = models.CharField(max_length=20, blank=True)
    metas_requeridos_posicion = models.ForeignKey(Puesto)

    def __str__(self):
        '''Regresar un identificador'''
        identidad = '%s %s' % (self.metas_reclutador_id, self.metas_fecha)
        return identidad


class Reclutado(models.Model):
    '''Lista de reclutados'''

    rec_nombres = models.CharField(max_length=40, blank=True)
    rec_apellido_paterno = models.CharField(max_length=30, blank=True)
    rec_apellido_materno = models.CharField(max_length=30, blank=True)
    rec_fecha_nacimiento = models.DateField(blank=True)
    rec_email = models.CharField(max_length=50, blank=True)
    rec_telefono = models.CharField(max_length=30, blank=True)
    rec_calle = models.CharField(max_length=30, blank=True)
    rec_numero = models.CharField(max_length=30, blank=True)
    rec_ciudad = models.CharField(max_length=30, blank=True)
    rec_estado = models.CharField(max_length=30, blank=True)
    rec_codigo_postal = models.CharField(max_length=30, blank=True)
    rec_fecha_entrevista = models.DateField(blank=True)
    rec_fecha_captacion = models.DateField(default=datetime.now, blank=True)
    rec_proyecto = models.CharField(max_length=10, blank=True)
    rec_proyecto_puesto = models.CharField(max_length=8, blank=True)
    rec_reclutador = models.CharField(max_length=30, blank=True)

    def __str__(self):
        '''regresar valor'''
        reclutado_id = '%s %s %s %s' % (
            self.id,
            self.rec_apellido_paterno,
            self.rec_apellido_materno,
            self.rec_nombres)
        return reclutado_id


class PuntoReclutamiento(models.Model):
    '''Tabla de referencia para la lista de punto de reclutamiento'''
    class Meta:
        '''Corregir plurales'''
        verbose_name_plural = 'Puntos de Reclutamiento'
    punto_reclutamiento = models.CharField(max_length=30, blank=True)

    def __str__(self):
        '''Regresar el punto'''
        return self.punto_reclutamiento


class Comunicacion(models.Model):
    '''Registro de Como se entero de la vacante'''
    como_se_entero = models.CharField(max_length=30, blank=True)

    def __str__(self):
        '''Regresar algo'''
        return self.como_se_entero


class Sueldos(models.Model):
    '''Texto'''
    class Meta:
        '''Corregir plurales'''
        verbose_name_plural = 'Sueldos'

    sueldos_proyecto = models.ForeignKey(Proyecto)
    sueldos_puesto = models.ForeignKey(Puesto)
    sueldos_salario_diario = models.CharField(max_length=10, blank=True)
    sueldos_bonos = models.CharField(max_length=10, blank=True)
    sueldos_total_efectivo = models.CharField(max_length=10, blank=True)

    def __str__(self):
        '''regresar nombre'''
        sueldo_id = '%s %s' % (self.sueldos_proyecto, self.sueldos_puesto)
        return sueldo_id


class Prestaciones(models.Model):
    '''texto'''
    class Meta:
        '''Corregir plurales'''
        verbose_name_plural = 'Prestaciones'

    prestaciones_proyecto = models.ForeignKey(Proyecto)
    prestaciones_nombre = models.CharField(max_length=30, blank=True)
    prestacion_imagen = models.FileField(
        upload_to='Tecmaiconos/')

    def __str__(self):
        '''Regresar identificador'''
        prestaciones_id = '%s %s' % (
            self.prestaciones_proyecto, self.prestaciones_nombre)
        return prestaciones_id


class RecursosVideo(models.Model):
    ''' Registro de los recursos de video comunes a todo tecma '''
    recursotipo = (
        ('videoTecmaMain', 'Video Mi nueva casa'),
        ('videoTecmaEvent', 'Video Mi familia Tecma'))

    recursosvideo_nombre = models.CharField(max_length=40,
        choices=recursotipo)
    recursosvideo_descripcion = models.CharField(max_length=50)
    recursosvideo_url = models.URLField(blank=True)
    recursosvideo_archivo_qt = models.FileField(
        upload_to='TecmaGeneral/')
    recursosvideo_archivo_fx = models.FileField(
        upload_to='TecmaGeneral/')

    def __str__(self):
        ''' Regresar identificador '''
        recursoidentificador = '%s - %s' % (
            self.recursosvideo_nombre,
            self.recursosvideo_descripcion)

        return recursoidentificador


class ProcesoRH(models.Model):
    ''' Modelo de las acciones realizadas por Recursos Humano, se vincula
        con el perfil de cada prospecto para actualizar y agregar detalles
        del proceso de reclutamiento.
    '''
    fechahoy = datetime.now().date()
    procesorh_reclutado = models.ForeignKey(Reclutado)
    procesorh_llego = models.CharField(max_length=2)
    procesorh_cambiocita = models.DateField(blank=True, null=True)
    procesorh_entrevista = models.CharField(max_length=2)
    procesorh_contratado = models.CharField(max_length=2)
    procesorh_rechazo = models.CharField(max_length=50, blank=True)
    procesorh_notas = models.CharField(max_length=250, blank=True)
    procesorh_folio = models.DateField(default=datetime.now, blank=True)

    def __str__(self):
        ''' doc string '''
        identificacion = '%s - Cita: %s' % (
            self.procesorh_reclutado,
            self.procesorh_folio)

        return identificacion

    def __ini__(self):
        ''''''
        self.fields['procesorh_rechazo'].choices = [
            (r.pk, r.razonrechazo) for r in models.RazonRechazo.objects.all()]
