from django import forms
#from django.core.excepions import ValidationError
from TecmaMain import models

# Importar los modelos que se vayan a utilizar en las formas
#from TecmaMain import Perfil

# Funciones para las listas de opciones


class FormatoLogin(forms.Form):
    'Forma de login, usa el widget de enmascarar el password'
    nomusuario = forms.CharField(label='Usuario')
    passusuario = forms.CharField(
        label='Password',
        max_length=20,
        widget=forms.PasswordInput)


class RegistroReclutado(forms.Form):
    ''' Forma para registro de informacion del reclutado
        El campo proyecto de llena automatico tomando la informacion del
        contexto de la forma.
        El campo puesto sera un dropbox que muestre los puestos.
    '''
    class Meta:
        ''' Meta clase para generar la forma del modelo'''
        model = models.Reclutado
        fields = '__all__'

    frmrec_nombres = forms.CharField(
        label='Nombre(s)')
    frmrec_apellido_paterno = forms.CharField(
        label='Apellido Paterno')
    frmrec_apellido_materno = forms.CharField(
        label='Apellido Materno')
    frmrec_fecha_nacimiento = forms.DateField(
        label='Fecha de Nacimiento')
    frmrec_email = forms.EmailField(
        label='Correo Electronico')
    frmrec_telefono = forms.CharField(
        label='Telefono')
    frmrec_calle = forms.CharField(
        label='Domicilio (Calle)')
    frmrec_numero = forms.CharField(
        label='Numero')
    frmrec_ciudad = forms.ChoiceField(
        label='Ciudad',
        choices=())
    frmrec_estado = forms.ChoiceField(
        label='Estado',
        choices=())
    frmrec_codigo_postal = forms.CharField(
        label='Codigo Postal')
    frmrec_fecha_entrevista = forms.DateField(
        label='Fecha de entrevista')
    frmrec_fecha_captacion = forms.DateField(
        label='Fecha')
    frmrec_proyecto = forms.CharField(
        label='Proyecto')
    frmrec_comunicacion = forms.ChoiceField(
        label='Como se entero del puesto?',
        choices=())
    frmrec_puntoreclutamiento = forms.ChoiceField(
        label='Punto de Reclutamiento',
        choices=())
    frmrec_proyecto_puesto = forms.CharField(
        label='Puesto al que aplica')
    frmrec_reclutador = forms.CharField()

    def __init__(self, *args, **kwargs):
        ''' Listas de seleccion '''
        super(RegistroReclutado, self).__init__(*args, **kwargs)

        self.fields['frmrec_ciudad'].choices = [('', '---------')] +\
            [(c.pk, c.ciudad) for c in models.Ciudades.objects.all()]

        self.fields['frmrec_estado'].choices = [('', '---------')] +\
            [(c.pk, c.estado) for c in models.Estados.objects.all()]

        self.fields['frmrec_puntoreclutamiento'].choices = [('', '-------')] +\
            [(c.pk, c.punto_reclutamiento)
                for c in models.PuntoReclutamiento.objects.all()]

        self.fields['frmrec_comunicacion'].choices = [('', '-------')] +\
            [(c.pk, c.como_se_entero)
                for c in models.Comunicacion.objects.all()]


class ProcesoCandidato(forms.Form):
    ''''''

    hrfrmreclutado_nombres = forms.CharField(
        label='Nombres', required=False)
    hrfrmreclutado_apellido_paterno = forms.CharField(
        label='Apellido Paterno', required=False)
    hrfrmreclutado_apellido_materno = forms.CharField(
        label='Apellido Materno', required=False)
    hrfrmreclutado_edad = forms.CharField(
        label='Edad', required=False)
    hrfrmreclutado_email = forms.CharField(
        label='email', required=False)
    hrfrmreclutado_telefono = forms.CharField(
        label='Telefono', required=False)
    hrfrmreclutado_calle = forms.CharField(
        label='Calle', required=False)
    hrfrmreclutado_numero = forms.CharField(
        label='Numero', required=False)
    hrfrmreclutado_ciudad = forms.CharField(
        label='Ciudad', required=False)
    hrfrmreclutado_se_presento = forms.ChoiceField(
        label='Se Presento', required=False)
    hrfrmreclutado_cambio_de_cita = forms.DateField(
        label='Cambio de cita', required=False)
    hrfrmreclutado_entrevista = forms.ChoiceField(
        label='Entrevista', required=False)
    hrfrmreclutado_contratado = forms.ChoiceField(
        label='Contratado?', required=False)
    hrfrmreclutado_motivo_de_rechazo = forms.ChoiceField(
        label='Motivo de Rechazo', required=False)
    hrfrmreclutado_notas = forms.CharField(
        label='Notas', required=False)

    def __init__(self, *args, **kwargs):
        ''''''
        super(ProcesoCandidato, self).__init__(*args, **kwargs)

        self.fields['hrfrmreclutado_se_presento'].choices = [
            ('', '------'),
            ('Si', 'Si'),
            ('No', 'No'),
            ]
        self.fields['hrfrmreclutado_entrevista'].choices = [
            ('', '------'),
            ('Si', 'Si'),
            ('No', 'No'),
            ]
        self.fields['hrfrmreclutado_contratado'].choices = [
            ('', '------'),
            ('Si', 'Si'),
            ('No', 'No'),
            ]
        self.fields['hrfrmreclutado_motivo_de_rechazo'].choices = \
            [('', '------')] + [(c.pk, c.razonrechazo)
                for c in models.RazonRechazo.objects.all()]


class RegistroMetasReclutador(forms.Form):
    '''
        Forma para el registro de metas del reclutador
    '''

    class Meta:
        ''' Meta clase para generar la forma del modelo'''
        model = models.MetasReclutador
        fields = '__all__'

    frmmetas_fecha = forms.CharField(
        label='Fecha:')
    frmmetas_proyecto = forms.ChoiceField(
        label='Proyecto',
        choices=())
    frmmetas_puesto = forms.ChoiceField(
        label='Puesto',
        choices=())
    frmmetas_requeridos = forms.CharField(
        label='Requeridos')
    frmmetas_reclutador = forms.ChoiceField(
        label='Reclutador',
        choices=())

    def __init__(self, *args, **kwargs):
        ''' Algo'''
        super(RegistroMetasReclutador, self).__init__(*args, **kwargs)

        self.fields['frmmetas_proyecto'].choices = [('', '-------')] +\
            [(c.pk, c.proyecto_nombre)
                for c in models.Proyecto.objects.all()]

        self.fields['frmmetas_puesto'].choices = [('', '----')] +\
            [(c.pk, c.puesto_nombre)
                for c in models.Puesto.objects.all()]

        self.fields['frmmetas_reclutador'].choices = [('', '-------')] +\
            [(c.pk, c.first_name.__str__() + ' ' + c.last_name.__str__())
                for c in models.User.objects.all()]


class ReporteMetas(forms.Form):
    '''
        Forma para generar los reportes del coordinador
    '''

    frmreporte_fecha = forms.CharField(
        label='Fecha')
    frmreporte_periodo = forms.ChoiceField(
        label='Periodo',
        choices=())
    frmreporte_proyecto = forms.ChoiceField(
        label='Proyecto',
        choices=())
    frmreporte_reclutador = forms.ChoiceField(
        label='Reclutador',
        choices=())

    def __init__(self, *args, **kwargs):
        ''' juntar los valores de las listas a utilizar'''
        super(ReporteMetas, self).__init__(*args, **kwargs)

        self.fields['frmreporte_periodo'].choices = [('', 'Todos')] +\
            [(c.pk, c.periodo_nombre)
                for c in models.Periodos.objects.all()]

        self.fields['frmreporte_proyecto'].choices = [('', 'Todos')] +\
            [(c.pk, c.proyecto_nombre)
                for c in models.Proyecto.objects.all()]

        self.fields['frmreporte_reclutador'].choices = [('', 'Todos')] +\
            [(c.pk, c.first_name.__str__() + ' ' + c.last_name.__str__())
                for c in models.User.objects.all()]