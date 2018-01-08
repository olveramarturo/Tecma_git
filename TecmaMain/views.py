from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.db import connection
from TecmaMain.forms import (
    FormatoLogin, RegistroReclutado, ProcesoCandidato, RegistroMetasReclutador,
    ReporteMetas)
from datetime import datetime
from TecmaMain import models
import arrow

'''
    the context keyword is used to pass a list of values to the template
    this can include all the values that are to be displayed as elements in
    the app.
'''

# Create your views here.


def GetPeriodo(valFecha):
    '''
        Funcion general para identificar el periodo
        al que pertenece una fecha
    '''
    metasDATE = valFecha
    cur = connection.cursor()
    # Identificar periodo de fechas
    try:
        cur.execute(
            "select periodo_inicio, periodo_fin from TecmaMain_periodos" +
            " as a where periodo_inicio <=%s " +
            "AND periodo_fin >=%s", ([metasDATE], [metasDATE]))
        fecha = cur.fetchall()
        fechainicio = fecha[0][0].strftime('%Y-%m-%d')
        fechafin = fecha[0][1].strftime('%Y-%m-%d')
        cur.close()
        # Se regresan valores indentificados
        return fechainicio, fechafin
    except:
        msg = 'No hay registro del periodo'
        # Se regresa el mensaje de error
        return msg


def hrlists(fecha, request):
    ''' Funcion general para alimentar la lista de reclutados
        recibe dos parametros: la fecha y la solicitud
    '''
    # RH necesita la lista de registrados con fecha actual
    try:
        reclist = list(models.Reclutado.objects.filter(
            rec_fecha_entrevista=fecha).values())
    except:
        messages.warning(request, 'No hay candidatos agendados hoy')
        return HttpResponseRedirect('rhmain.html')

    #Iteracion por cada uno de los registros
    statuslist = {}
    for registro in reclist:
        idx = str(registro['id'])
        # Get project name
        try:
            projNombre = models.Proyecto.objects.get(
                id=registro['rec_proyecto'])
            projnombre = projNombre.proyecto_nombre
            print(projnombre)
        except:
            projnombre = 'No hay registro de proyecto'
            messages.error(request, 'No hay registros de proyecto')
            return HttpResponseRedirect('rhmain.html')
        # Get project job title
        try:
            projPuesto = models.Puesto.objects.get(
                id=int(registro['rec_proyecto_puesto']))
            projpuesto = projPuesto.puesto_nombre
            print(projpuesto)
        except:
            projpuesto = 'No hay registro de puesto'
            messages.error(request, 'No hay registros de proyecto')
            return HttpResponseRedirect('rhmain.html')
        # Get RH status (hired, processed, etc)
        try:
            rhStatus = models.ProcesoRH.objects.get(
                procesorh_reclutado=registro['id'])
            rhstatus = rhStatus.procesorh_contratado
        except:
            rhstatus = 'No procesado'
        # Get rejection status
        try:
            rhRechazo = rhStatus.procesorh_rechazo
            rhrechazocode = models.RazonRechazo.objects.get(pk=rhRechazo)
            rhrechazo = rhrechazocode.razonrechazo
            print(rhRechazo)
        except:
            rhrechazo = ''

        # Armar el diccionario con los resultados
        tester = [str(idx), fecha.isoformat(),
            registro['rec_apellido_paterno'],
            registro['rec_apellido_materno'], registro['rec_nombres'],
            projnombre, projpuesto, rhstatus, rhrechazo]
        statuslist[idx] = tester

    return (statuslist)


@login_required(login_url='/login/')
def base(request):
    '''Funcion de renderizacion de prueba'''
    tituloHTML = 'Plantilla'
    return render(request, 'tecmabase.html', {
        'titulo': tituloHTML,
        'marca': 'Plataforma Electronica de Reclutamiento',
        'section': 'Base'})


@login_required(login_url='/login/')
def reclutadormain(request):
    ''' Recolleccion de la informacion requerida para la pagina principal
        del reclutador. Debe de reunir la informacion para los iconos y links
        de cada proyecto
    '''
    # Valores de los encabzados y titulos
    tituloHTML = 'Reclutador'
    currentuser = request.user

    # Recoleccion de la informacion de proyectos
    listaproyectos = models.Proyecto.objects.all().values(
        'id',
        'proyecto_nombre',
        'proyecto_img')

    # Retorno de valores hacia la pagina
    return render(request, 'sitio_reclutador/reclutadormain.html', {
        'titulo': tituloHTML,
        'marca': 'Plataforma Electronica de Reclutamiento',
        'section': 'Reclutador',
        'username': currentuser,
        'listaproyectos': listaproyectos})


@login_required(login_url='/login/')
def rhmain(request):
    '''Funcion de renderizacion de Recursos Humanos'''
    tituloHTML = 'Recursos Humanos'
    fechahoy = datetime.now().date()
    # Identifica si la solicitud es un GET o un POST
    # POST = Se selecciona alguna fecha
    # GET = Por default se listan los registros del
    if request.method == 'POST':
        fechahoy = request.POST.get('filtrofecha', '')
        # RH necesita la lista de registrados con fecha actual
        try:
            reclist = list(models.Reclutado.objects.filter(
                rec_fecha_entrevista=fechahoy).values())
        except:
            messages.warning(request, 'No hay candidatos agendados hoy')
            return HttpResponseRedirect('rhmain.html')
        #Iteracion por cada uno de los registros
        statuslist = {}
        for registro in reclist:
            idx = str(registro['id'])
            # Get project name
            try:
                projNombre = models.Proyecto.objects.get(
                    id=registro['rec_proyecto'])
                projnombre = projNombre.proyecto_nombre
            except:
                projnombre = 'No hay registro de proyecto'
            # Get project job title
            try:
                projPuesto = models.Puesto.objects.get(
                    id=int(registro['rec_proyecto_puesto']))
                projpuesto = projPuesto.puesto_nombre
            except:
                projpuesto = 'No hay registro de puesto'
            # Get RH status (hired, processed, etc)
            try:
                rhStatus = models.ProcesoRH.objects.get(
                    procesorh_reclutado=registro['id'])
                rhstatus = rhStatus.procesorh_contratado
            except:
                rhstatus = 'No procesado'
            # Get rejection status
            try:
                rhRechazo = rhStatus.procesorh_rechazo
                rhrechazocode = models.RazonRechazo.objects.get(pk=rhRechazo)
                rhrechazo = rhrechazocode.razonrechazo
            except:
                rhrechazo = ''
            # Assemble results in dictionary
            tester = [str(idx), fechahoy,
                registro['rec_apellido_paterno'],
                registro['rec_apellido_materno'], registro['rec_nombres'],
                projnombre, projpuesto, rhstatus, rhrechazo]
            statuslist[idx] = tester
            # *** Fin the la iteracion por cada registro ***

        # Total enviados en el dia actual
        cntCandidatos = models.Reclutado.objects.filter(
            rec_fecha_entrevista=fechahoy).count()
        # Conteo de Rechazados
        c = connection.cursor()
        c.execute(
            "SELECT COUNT(a.id) FROM TecmaMain_reclutado a " +
            "LEFT JOIN TecmaMain_procesorh b " +
            "ON a.id = b.procesorh_reclutado_id " +
            "WHERE a.rec_fecha_entrevista = %s" +
            "AND b.procesorh_rechazo != ''", [fechahoy])
        cnt_nocontratados = c.fetchall()
        cnt_nocontratos = cnt_nocontratados[0][0]
        # Conteo Contratados
        contrato = 'Si'
        c.execute(
            "SELECT COUNT(a.id) FROM TecmaMain_reclutado a " +
            "LEFT JOIN TecmaMain_procesorh b " +
            "ON a.id = b.procesorh_reclutado_id " +
            "WHERE a.rec_fecha_entrevista = %s " +
            "AND b.procesorh_contratado = %s", ([fechahoy], [contrato]))
        cnt_Contratados = c.fetchall()
        cnt_contratados = cnt_Contratados[0][0]
        # Procesados
        cntprocesados = cnt_nocontratos + cnt_contratados
        # Ratio
        try:
            cntratio = (int(cnt_contratados) / int(cntCandidatos))
            #cntratio = (int(cntCandidatos) / int(cnt_contratados))
        except:
            cntratio = '0'

        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Seccion de conteos por periodo
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Identificar periodo de fechas
        try:
            c.execute(
                "select periodo_inicio, periodo_fin from TecmaMain_periodos" +
                " as a where periodo_inicio <=%s " +
                "AND periodo_fin >=%s;", ([fechahoy], [fechahoy]))
            fecha = c.fetchall()
            fechainicio = fecha[0][0].strftime('%Y-%m-%d')
            fechafin = fecha[0][1].strftime('%Y-%m-%d')
        except:
            messages.warning(request, 'No hay registro del periodo')
        # Conteo de enviados
        try:
            c.execute(
                "select id from TecmaMain_reclutado " +
                "where rec_fecha_entrevista >= %s " +
                "and rec_fecha_entrevista <= %s", ([fechainicio], [fechafin]))
            periodoCuenta = c.fetchall()
            enviadosperiodo = 0
            for i in periodoCuenta:
                enviadosperiodo = enviadosperiodo + 1
        except:
            enviadosperiodo = 0
            print('No se pudo obtener la cuenta de enviados en el periodo')
        # Conteo contratados en el periodo
        try:
            c.execute(
                "SELECT count(id) FROM " +
                "(SELECT res.id as id, rh.procesorh_contratado, " +
                "rh.procesorh_rechazo FROM TecmaMain_reclutado res " +
                "LEFT JOIN TecmaMain_procesorh rh " +
                "ON res.id = rh.procesorh_reclutado_id " +
                "WHERE res.rec_fecha_entrevista >= %s " +
                "AND res.rec_fecha_entrevista <= %s) AS rhlist " +
                "WHERE procesorh_contratado IS NOT Null ", (
                    [fechainicio], [fechafin]))
            periodoContrato = c.fetchall()
            periodocontrato = periodoContrato[0][0]
            print(periodocontrato)
        except:
            periodocontrato = 0
            print('No se pudo obtener la cuenta de enviados en el periodo')
            print(periodocontrato)

        # Conteo Rechazados en el periodo
        try:
            c.execute(
                "SELECT count(id) FROM " +
                "(SELECT res.id as id, rh.procesorh_contratado, " +
                "rh.procesorh_rechazo FROM TecmaMain_reclutado res " +
                "LEFT JOIN TecmaMain_procesorh rh " +
                "ON res.id = rh.procesorh_reclutado_id " +
                "WHERE res.rec_fecha_entrevista >= %s " +
                "AND res.rec_fecha_entrevista <= %s) AS rhlist " +
                "WHERE procesorh_contratado = 'No' ", (
                    [fechainicio], [fechafin]))
            periodoRechazo = c.fetchall()
            periodorechazo = periodoRechazo[0][0]
            print(periodorechazo)
        except:
            periodoProcess = 0
            print('No se pudo obtener la cuenta de enviados en el periodo')
            print(periodorechazo)

        # Conteo Procesados en el Periodo
        periodoprocesados = periodorechazo + periodocontrato

        try:
            periodoratio = (int(periodocontrato) / int(enviadosperiodo))
            print(periodoratio)
            #periodoratio = (int(enviadosperiodo) / int(periodocontrato))
        except ZeroDivisionError:
            periodoratio = '0'

        return render(request, 'sitio_rh/rhmain.html', {
            'username': request.user,
            'titulo': tituloHTML,
            'marca': 'Plataforma Electronica de Reclutamiento',
            'section': 'Recursos Humanos',
            'rh_candidatos': statuslist,
            'cntcandidatos': cntCandidatos,
            'cntnocontrato': cnt_nocontratos,
            'cntcontratados': cnt_contratados,
            'cntprocesados': cntprocesados,
            'cntratio': cntratio,
            'periodoenviados': enviadosperiodo,
            'periodocontratos': periodocontrato,
            'periodorechazos': periodorechazo,
            'periodoprocesados': periodoprocesados,
            'periodoratio': periodoratio})

    #**************************************************************************
    # Seccion de info default (del dia en curso)
    #**************************************************************************
    else:
        print('**** Seccion default - GET ***')
        # RH necesita la lista de registrados con fecha actual
        try:
            reclist = list(models.Reclutado.objects.filter(
                rec_fecha_entrevista=fechahoy).values())
        except:
            messages.warning(request, 'No hay candidatos agendados hoy')
            return HttpResponseRedirect('rhmain.html')

        #Iteracion por cada uno de los registros
        statuslist = {}
        for registro in reclist:
            idx = str(registro['id'])

            # Get project name
            try:
                projNombre = models.Proyecto.objects.get(
                    id=registro['rec_proyecto'])
                projnombre = projNombre.proyecto_nombre
                #print(projnombre)
            except:
                projnombre = 'No hay registro de proyecto'
                messages.error(request, 'No hay registros de proyecto')
                return HttpResponseRedirect('rhmain.html')

            # Get project job title
            try:
                projPuesto = models.Puesto.objects.get(
                    id=int(registro['rec_proyecto_puesto']))
                projpuesto = projPuesto.puesto_nombre
                #print(projpuesto)
            except:
                projpuesto = 'No hay registro de puesto'
                messages.error(request, 'No hay registros de proyecto')
                return HttpResponseRedirect('rhmain.html')

            # Get RH status (hired, processed, etc)
            try:
                rhStatus = models.ProcesoRH.objects.get(
                    procesorh_reclutado=registro['id'])
                rhstatus = rhStatus.procesorh_contratado
            except:
                rhstatus = 'No procesado'

            # Get rejection status
            try:
                rhRechazo = rhStatus.procesorh_rechazo
                rhrechazocode = models.RazonRechazo.objects.get(pk=rhRechazo)
                rhrechazo = rhrechazocode.razonrechazo
            except:
                rhrechazo = ''

            # Assemble results in dictionary
            tester = [str(idx), fechahoy.isoformat(),
                registro['rec_apellido_paterno'],
                registro['rec_apellido_materno'], registro['rec_nombres'],
                projnombre, projpuesto, rhstatus, rhrechazo]
            statuslist[idx] = tester
        # Total enviados en el dia actual
        cntCandidatos = models.Reclutado.objects.filter(
            rec_fecha_entrevista=fechahoy).count()
        # Conteo de Rechazados
        c = connection.cursor()
        c.execute(
            "SELECT COUNT(a.id) FROM TecmaMain_reclutado a " +
            "LEFT JOIN TecmaMain_procesorh b " +
            "ON a.id = b.procesorh_reclutado_id " +
            "WHERE a.rec_fecha_entrevista = %s" +
            "AND b.procesorh_rechazo != ''", [fechahoy])
        cnt_nocontratados = c.fetchall()
        cnt_nocontratos = cnt_nocontratados[0][0]
        #print(("No Contratados: %s", cnt_nocontratos))
        # Conteo Contratados
        contrato = 'Si'
        c.execute(
            "SELECT COUNT(a.id) FROM TecmaMain_reclutado a " +
            "LEFT JOIN TecmaMain_procesorh b " +
            "ON a.id = b.procesorh_reclutado_id " +
            "WHERE a.rec_fecha_entrevista = %s " +
            "AND b.procesorh_contratado = %s", ([fechahoy], [contrato]))
        cnt_Contratados = c.fetchall()
        cnt_contratados = cnt_Contratados[0][0]
        # Procesados
        cntprocesados = cnt_nocontratos + cnt_contratados
        # Ratio
        try:
            cntratio = (int(cnt_contratados) / int(cntCandidatos))
        except:
            cntratio = '0'

        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Seccion de conteos por periodo
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        # Identificar periodo de fechas
        try:
            c.execute(
                "select periodo_inicio, periodo_fin from TecmaMain_periodos" +
                " as a where periodo_inicio <= curdate() " +
                "AND periodo_fin >= curdate();")
            fecha = c.fetchall()
            fechainicio = fecha[0][0].strftime('%Y-%m-%d')
            fechafin = fecha[0][1].strftime('%Y-%m-%d')
        except:
            messages.warning(request, 'No hay registro del periodo')

        # Conteo enviados del periodo
        try:
            c.execute(
                "select id from TecmaMain_reclutado " +
                "where rec_fecha_entrevista >= %s " +
                "and rec_fecha_entrevista <= %s", ([fechainicio], [fechafin]))
            periodoCuenta = c.fetchall()
            enviadosperiodo = 0
            for i in periodoCuenta:
                enviadosperiodo = enviadosperiodo + 1
        except:
            enviadosperiodo = 0
            print('No se pudo obtener la cuenta de enviados en el periodo')

        # Conteo Procesados en el periodo (contratado+rechazado)
        try:
            c.execute(
                "SELECT count(id) FROM " +
                "(SELECT res.id as id, rh.procesorh_contratado, " +
                "rh.procesorh_rechazo FROM TecmaMain_reclutado res " +
                "LEFT JOIN TecmaMain_procesorh rh " +
                "ON res.id = rh.procesorh_reclutado_id " +
                "WHERE res.rec_fecha_entrevista >= %s " +
                "AND res.rec_fecha_entrevista <= %s) AS rhlist " +
                "WHERE procesorh_contratado != Null " +
                "OR procesorh_rechazo != Null", ([fechainicio], [fechafin]))
            periodoProcess = c.fetchall()
            print(periodoProcess)
        except:
            periodoProcess = 0
            print('No se pudo obtener la cuenta de enviados en el periodo')
            print(periodoProcess)

        # Conteo contratados en el periodo
        try:
            c.execute(
                "SELECT count(id) FROM " +
                "(SELECT res.id as id, rh.procesorh_contratado, " +
                "rh.procesorh_rechazo FROM TecmaMain_reclutado res " +
                "LEFT JOIN TecmaMain_procesorh rh " +
                "ON res.id = rh.procesorh_reclutado_id " +
                "WHERE res.rec_fecha_entrevista >= %s " +
                "AND res.rec_fecha_entrevista <= %s) AS rhlist " +
                "WHERE procesorh_contratado IS NOT Null ", (
                    [fechainicio], [fechafin]))
            periodoContrato = c.fetchall()
            periodocontrato = periodoContrato[0][0]
            print(periodocontrato)
        except:
            periodocontrato = 0
            print('No se pudo obtener la cuenta de enviados en el periodo')
            print(periodocontrato)

        # Conteo Rechazados en el periodo
        try:
            c.execute(
                "SELECT count(id) FROM " +
                "(SELECT res.id as id, rh.procesorh_contratado, " +
                "rh.procesorh_rechazo FROM TecmaMain_reclutado res " +
                "LEFT JOIN TecmaMain_procesorh rh " +
                "ON res.id = rh.procesorh_reclutado_id " +
                "WHERE res.rec_fecha_entrevista >= %s " +
                "AND res.rec_fecha_entrevista <= %s) AS rhlist " +
                "WHERE procesorh_contratado = 'No' ", (
                    [fechainicio], [fechafin]))
            periodoRechazo = c.fetchall()
            periodorechazo = periodoRechazo[0][0]
            print(periodorechazo)
        except:
            periodoProcess = 0
            print('No se pudo obtener la cuenta de enviados en el periodo')
            print(periodorechazo)

        # Conteo Procesados en el Periodo
        periodoprocesados = periodorechazo + periodocontrato
        try:
            periodoratio = (int(periodocontrato) / int(enviadosperiodo))
        except:
            periodoratio = '0'

        return render(request, 'sitio_rh/rhmain.html', {
            'username': request.user,
            'titulo': tituloHTML,
            'marca': 'Plataforma Electronica de Reclutamiento',
            'section': 'Recursos Humanos',
            'rh_candidatos': statuslist,
            'cntcandidatos': cntCandidatos,
            'cntnocontrato': cnt_nocontratos,
            'cntcontratados': cnt_contratados,
            'cntprocesados': cntprocesados,
            'cntratio': cntratio,
            'periodoenviados': enviadosperiodo,
            'periodocontratos': periodocontrato,
            'periodorechazos': periodorechazo,
            'periodoprocesados': periodoprocesados,
            'periodoratio': periodoratio})


@login_required(login_url='/login/')
def procesorh(request):
    ''''''
    if request.method == 'POST':
        reclutadoid = request.POST.get('candidatoid', '')
        print(reclutadoid)
        form = ProcesoCandidato(request.POST)
        if form.is_valid():
            #Recuperamos el objeto para modificarlo segun el ID del reclutado
            objreclutado = models.Reclutado.objects.get(
                pk=reclutadoid)
            # Lo mismo para la info del proceso RH
            objrh = models.ProcesoRH.objects.get(
                procesorh_reclutado=reclutadoid)
            # Se actualizan los valores en las dos instancias
            objreclutado.rec_nombres = form.cleaned_data[
                'hrfrmreclutado_nombres']
            objreclutado.rec_apellido_paterno = form.cleaned_data[
                'hrfrmreclutado_apellido_paterno']
            objreclutado.rec_apellido_materno = form.cleaned_data[
                'hrfrmreclutado_apellido_materno']
            objreclutado.rec_email = form.cleaned_data[
                'hrfrmreclutado_email']
            objreclutado.rec_telefono = form.cleaned_data[
                'hrfrmreclutado_telefono']
            objreclutado.rec_calle = form.cleaned_data[
                'hrfrmreclutado_calle']
            objreclutado.rec_numero = form.cleaned_data[
                'hrfrmreclutado_numero']
            objreclutado.rec_ciudad = form.cleaned_data[
                'hrfrmreclutado_ciudad']
            objrh.procesorh_llego = form.cleaned_data[
                'hrfrmreclutado_se_presento']
            objrh.procesorh_cambiocita = form.cleaned_data[
                'hrfrmreclutado_cambio_de_cita']
            objrh.procesorh_entrevista = form.cleaned_data[
                'hrfrmreclutado_entrevista']
            objrh.procesorh_contratado = form.cleaned_data[
                'hrfrmreclutado_contratado']
            objrh.procesorh_rechazo = form.cleaned_data[
                'hrfrmreclutado_motivo_de_rechazo']
            objrh.procesorh_notas = form.cleaned_data[
                'hrfrmreclutado_notas']

            try:
                objreclutado.save()
                objrh.save()
                messages.success(request, 'Registro actualizado')
                return HttpResponseRedirect('rhmain.html')

            except (RuntimeError, TypeError, NameError):
                messages.error(request, 'No se relizo la actualizacion')
                return HttpResponseRedirect('rhmain.html')

        else:
            return HttpResponse('Form is not valid')
    else:
        # La solicitud es un GET
        reclutadoid = request.GET['candidato']
        procesodata = models.ProcesoRH.objects.filter(
            procesorh_reclutado_id=reclutadoid)
        # Verificar la instancia para el proceso RH
        if procesodata.exists() is False:
            objproceso = models.ProcesoRH()
            objproceso.procesorh_reclutado_id = reclutadoid
            objproceso.save()
            print('procesodata created')
        else:
            # Si ya existe procesodata, verificamos si ya esta procesado
            procesodata = models.ProcesoRH.objects.get(
                procesorh_reclutado_id=reclutadoid)

            if (procesodata.procesorh_contratado != ''
                or procesodata.procesorh_rechazo != ''):
                    return HttpResponse('El candidato ya fue procesado')
            else:
                # Si el reclutado no esta procesado, continuamos
                pass

        reclutadodata = models.Reclutado.objects.get(pk=reclutadoid)
        reclutadonacimiento = reclutadodata.rec_fecha_nacimiento
        fechaactual = datetime.now().date()
        deltaedad = (fechaactual - reclutadonacimiento)
        edad = int(deltaedad.days) / 365
        form = ProcesoCandidato()

    return render(request, 'sitio_rh/rhprocess.html', {
        'form': form,
        'username': request.user,
        'titulo': 'Proceso de Entrevista - RH',
        'marca': 'Plataforma electronica de Reclutamiento',
        'section': 'Proceso RH',
        'candidatoinfo': reclutadodata,
        'rhdata': procesodata,
        'reclutadoedad': edad.__int__()
        })


@login_required(login_url='/login/')
def coordinarmain(request):
    '''Funcion de renderizacion de coordinador'''
    listaproyectos = models.Proyecto.objects.all().values(
        'id',
        'proyecto_nombre',
        'proyecto_img')
    listareclutador = User.objects.filter(
        groups__name="Reclutador",
        is_active=True).values("id", "last_name", "first_name")
    tituloHTML = 'Coordinador'
    return render(request, 'sitio_coordinador/coordinarmain.html', {
        'titulo': tituloHTML,
        'username': request.user,
        'proyectos': listaproyectos,
        'reclutadores': listareclutador,
        'marca': 'Plataforma Electronica de Reclutamiento',
        'section': 'Coordinador'})


def user_login(request):
    ''' Proceso de login'''
    # Si la solicitud es POST, se instancia el objeto form y se toman los
    # datos
    if request.method == 'POST':
        form = FormatoLogin(request.POST)
        # Verificar los datos regresados en la forma
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                username=cd['nomusuario'],
                password=cd['passusuario']
                )
            # Si el usuario es != Ninguno
            if user is not None:
                # Si el usuario esta activo
                if user.is_active:
                    login(request, user)
                    #lista de usuarios por grupo de seguridad
                    groups = Group.objects.all()
                    # Evaluacion usuarioID pertenece a grupo
                    for group in groups:
                        if request.user.groups.filter(
                            name='Reclutador').exists():
                            base_url = '/sitio_reclutador/reclutadormain.html'
                        elif request.user.groups.filter(
                            name='Coordinador').exists():
                            base_url = '/sitio_coordinador/coordinarmain.html'
                        elif request.user.groups.filter(name='RH').exists():
                            base_url = '/sitio_rh/rhmain.html'
                        elif request.user.groups.filter(name='Admin').exists():
                            base_url = '/admin/'
                    # Fin ciclo FOR
                    return redirect(base_url)
                else:
                    # Si el usuario NO esta activo
                    messages.warning(request, 'El usuario no esta activo')
                    return HttpResponseRedirect('login.html')
            else:
                # Si el usuario NO existe o esta en blanco
                messages.warning(request, 'Revise el ID de usuario')
                return HttpResponseRedirect('login.html')
    else:
        # Si el request es de tipo GET, se instancia la forma en blanco
        form = FormatoLogin()

    return render(request, 'tecmalogin.html', {
        'form': form,
        'marca': 'Plataforma Electronica de Reclutamiento',
        'form_id': 'loginfrm'})


@login_required(login_url='/login/')
def user_logout(request):
    '''Funcion de logout'''
    logout(request)
    return render(request, 'tecmalogout.html', {
    'marca': 'Plataforma Electronica de Reclutamiento'})


@login_required(login_url='/login/')
def DetalleProyecto(request):
    '''Funcion llamada al presionar el icono del proyecto, el cual usa
       el nombre del proyecto como argumento para el GET. Luego este valor
       se recupera para seleccionar los valores que deben de vincular las
       siguientes ventanas.
    '''
    # Usuario logeado
    currentuser = request.user
    # Recpuperamos el ID del proyecto de la solicitud GET
    proyectoid = request.GET['proyecto']
    # Buscamos la info del proyecto segun el ID = PK
    proyectodata = models.Proyecto.objects.get(pk=proyectoid)

    return render(request, 'sitio_reclutador/detalleproyecto.html', {
        'username': currentuser,
        'proyectoID': proyectoid,
        'proyectoDATA': proyectodata,
        'marca': 'Plataforma Electronica de Reclutamiento'
        })


@login_required(login_url='/login/')
def metasview(request):
    ''' Busqueda de metas registradas para el usuario actual. Se asume que
        la primera llamada es un GET, si se usa el selector de fechas se
        genera una condicion de filtrado
    '''
    # Evaluar el metodo si es un GET o un POST
    #==========================================================================
    if request.method == 'POST':
        metasDATE = request.POST.get('filtrofecha', '')
        userID = request.POST.get('userid', '')
        #captura la fecha actual para usarla de filtro de metas
        #fechahoy = datetime.now().date()
        c = connection.cursor()
        # Identificar periodo de fechas
        try:
            c.execute(
                "select periodo_inicio, periodo_fin from TecmaMain_periodos" +
                " as a where periodo_inicio <=%s " +
                "AND periodo_fin >=%s", ([metasDATE], [metasDATE]))
            fecha = c.fetchall()
            fechainicio = fecha[0][0].strftime('%Y-%m-%d')
            fechafin = fecha[0][1].strftime('%Y-%m-%d')

        except:
            messages.warning(request, 'No hay registro del periodo')
        # Dataset de metas: Referenciando al usuario, se agrupan por proyecto y
        # se identifica el id de la mas reciente de cada proyecto.
        c = connection.cursor()
        c.execute(
            "SELECT auser.id, auser.first_name, auser.last_name, " +
            "metas.metas_requeridos, metas.metas_requeridos_posicion_id, " +
            "metas.metaID, metas.metas_proyecto_id, metas.proyecto_nombre " +
            "FROM auth_user AS auser RIGHT JOIN (SELECT a.metas_requeridos, " +
            "a.metas_requeridos_posicion_id, MAX(a.id) AS metaID, " +
            "a.metas_proyecto_id, a.metas_reclutador_id, b.proyecto_nombre " +
            "FROM TecmaMain_metasreclutador a right join " +
            "TecmaMain_proyecto b ON a.metas_proyecto_id = b.id WHERE " +
            "a.metas_reclutador_id = %s AND (a.metas_fecha >= %s " +
            "AND a.metas_fecha <= %s) GROUP BY a.metas_proyecto_id," +
            " a.metas_requeridos_posicion_id ORDER BY a.metas_proyecto_id, " +
            "a.id) as metas ON auser.id = metas_reclutador_id", (
                [userID.__str__()], [fechainicio], [fechafin]))
        metas = c.fetchall()
        print(metas)
        # Generar reporte de metas
        reportelist = {}
        idx = 0
        for linea in metas:
            # Nombre del puesto
            pjPuesto = models.Puesto.objects.get(pk=linea[4],
                puesto_proyecto_id=linea[6]).puesto_nombre
            # ID del puesto
            pjPuestoID = linea[4]
            # ID del proyecto
            pyProyectoID = linea[6]
            # Nombre del proyecto
            pyProyecto = linea[7]
            # Cuenta de metas
            cntMetas = linea[3]
            # Obtener conteos por dia
            c.execute(
                "SELECT count(prh.procesorh_contratado) AS contratados," +
                "count(prh.procesorh_rechazo) AS rechazados, count(tr.id) " +
                "AS enviados from TecmaMain_reclutado tr left join " +
            "TecmaMain_procesorh prh ON tr.id = prh.procesorh_reclutado_id" +
                " where rec_proyecto=%s AND rec_proyecto_puesto=%s AND " +
                "rec_fecha_entrevista=%s and rec_reclutador = %s", (
                    [pyProyectoID], [pjPuestoID], [metasDATE], [userID]))
            contdia = c.fetchall()
            try:
                ratiodia = contdia[0][2] / contdia[0][0]
            except:
                ratiodia = 0
            # Obtener conteos por periodo
            c.execute(
                "SELECT count(prh.procesorh_contratado) AS contratados, " +
                "count(prh.procesorh_rechazo) AS rechazados, count(tr.id) " +
                "AS enviados FROM TecmaMain_reclutado AS tr LEFT JOIN " +
                "TecmaMain_procesorh prh ON " +
                "tr.id = prh.procesorh_reclutado_id where rec_proyecto=%s " +
                "AND rec_proyecto_puesto=%s AND (rec_fecha_entrevista>=%s " +
                "AND rec_fecha_entrevista <= %s) AND rec_reclutador = %s", (
                    [pyProyectoID], [pjPuestoID], [fechainicio],
                    [fechafin], [userID]))
            contperiodo = c.fetchall()
            try:
                ratioperiodo = contperiodo[0][0] / contperiodo[0][2]
            except:
                ratioperiodo = 0
            # Armar linea
            repoLinea = [str(idx), pyProyecto, pjPuesto, cntMetas,
                contdia[0][2], contdia[0][0], contperiodo[0][2],
                contperiodo[0][0], ratiodia, ratioperiodo]
            reportelist[idx] = repoLinea
            idx = idx + 1
        #Fin FOR
        #Se tienen que ubicar los contratados
        return render(request, 'sitio_reclutador/metasreclutador.html', {
            'usuario': request.user,
            'reporte': reportelist
            })

    #==========================================================================
    # Si el request no es un POST
    #==========================================================================
    else:
        # Una solicitud get regresa los requerimeintos totales del periodo
        # Se recupera el ID del usuario
        userid = User.objects.get(username=request.user)
        userID = userid.pk
        #captura la fecha actual para usarla de filtro de metas
        metasDATE = datetime.now().date()
        c = connection.cursor()
        # Identificar periodo de fechas
        try:
            c.execute(
                "select periodo_inicio, periodo_fin from TecmaMain_periodos" +
                " as a where periodo_inicio <= curdate() " +
                "AND periodo_fin >= curdate();")
            fecha = c.fetchall()
            fechainicio = fecha[0][0].strftime('%Y-%m-%d')
            fechafin = fecha[0][1].strftime('%Y-%m-%d')
        except:
            messages.warning(request, 'No hay registro del periodo')
        # Dataset de metas: Referenciando al usuario, se agrupan por proyecto y
        # se identifica el id de la mas reciente de cada proyecto.
        c = connection.cursor()
        c.execute("SELECT auser.id, auser.first_name, auser.last_name, " +
            "metas.metas_requeridos, metas.metas_requeridos_posicion_id, " +
            "metas.metaID, metas.metas_proyecto_id, metas.proyecto_nombre " +
            "FROM auth_user AS auser RIGHT JOIN (SELECT a.metas_requeridos, " +
            "a.metas_requeridos_posicion_id, MAX(a.id) AS metaID, " +
            "a.metas_proyecto_id, a.metas_reclutador_id, b.proyecto_nombre " +
            "FROM TecmaMain_metasreclutador a right join " +
            "TecmaMain_proyecto b ON a.metas_proyecto_id = b.id WHERE " +
            "a.metas_reclutador_id = %s AND (a.metas_fecha >= %s " +
            "AND a.metas_fecha <= %s) GROUP BY a.metas_proyecto_id," +
            " a.metas_requeridos_posicion_id ORDER BY a.metas_proyecto_id, " +
            "a.id) as metas ON auser.id = metas_reclutador_id", (
                [userID.__str__()], [fechainicio], [fechafin]))
        metas = c.fetchall()
        # Generar reporte de metas
        reportelist = {}
        idx = 0
        for linea in metas:
            # Nombre del puesto
            pjPuesto = models.Puesto.objects.get(
                pk=linea[4], puesto_proyecto_id=linea[6]).puesto_nombre
            # ID del puesto
            pjPuestoID = linea[4]
            # ID del proyecto
            pyProyectoID = linea[6]
            # Nombre del proyecto
            pyProyecto = linea[7]
            # Cuenta de metas
            cntMetas = linea[3]
            # Obtener conteos por dia
            c.execute("SELECT count(prh.procesorh_contratado) as contratados," +
                "count(prh.procesorh_rechazo) as rechazados, count(tr.id) as" +
                " enviados from TecmaMain_reclutado tr left join " +
            "TecmaMain_procesorh prh ON tr.id = prh.procesorh_reclutado_id" +
                " where rec_proyecto=%s AND rec_proyecto_puesto=%s AND " +
                "rec_fecha_entrevista=%s and rec_reclutador = %s", (
                    [pyProyectoID], [pjPuestoID], [metasDATE], [userID]))
            contdia = c.fetchall()
            print(contdia)
            try:
                ratiodia = contdia[0][0] / contdia[0][2]
            except:
                ratiodia = 0
            # Obtener conteos por periodo
            c.execute(
                "SELECT count(prh.procesorh_contratado) AS contratados, " +
                "count(prh.procesorh_rechazo) AS rechazados, count(tr.id) " +
                "AS enviados FROM TecmaMain_reclutado AS tr LEFT JOIN " +
                "TecmaMain_procesorh prh ON " +
                "tr.id = prh.procesorh_reclutado_id where rec_proyecto=%s " +
                "AND rec_proyecto_puesto=%s AND (rec_fecha_entrevista>=%s " +
                "AND rec_fecha_entrevista <= %s) AND rec_reclutador = %s", (
                    [pyProyectoID], [pjPuestoID], [fechainicio],
                    [fechafin], [userID]))
            contperiodo = c.fetchall()
            try:
                ratioperiodo = contperiodo[0][0] / contperiodo[0][2]
            except:
                ratioperiodo = 0
            # Armar linea
            repoLinea = [str(idx), pyProyecto, pjPuesto, cntMetas,
                contdia[0][2], contdia[0][0], contperiodo[0][2],
                contperiodo[0][0], ratiodia, ratioperiodo]
            reportelist[idx] = repoLinea
            print(repoLinea)
            idx = idx + 1
        #Fin FOR
        #Se tienen que ubicar los contratados
        return render(request, 'sitio_reclutador/metasreclutador.html', {
            'usuario': request.user,
            'reporte': reportelist
            })


@login_required(login_url='/login/')
def reclutarview(request):
    '''Vista utilizada para generar la pantalla de reclutamiento'''
    if request.method == 'POST':
        pyID = request.POST.get('frmrec_proyecto', '')
        print('----------------------------------------------------')
        print(pyID)
        form = RegistroReclutado(request.POST)
        if form.is_valid():
            # Procesar la forma
            objrec = models.Reclutado()  # instanciar el modelo Reclutado
            objrepo = models.ReporteContacto()  # Instanciar como se entero
            objrec.rec_nombres = form.cleaned_data['frmrec_nombres']
            objrec.rec_apellido_paterno = form.cleaned_data[
                'frmrec_apellido_paterno']
            objrec.rec_apellido_materno = form.cleaned_data[
                'frmrec_apellido_materno']
            objrec.rec_fecha_nacimiento = form.cleaned_data[
                'frmrec_fecha_nacimiento']
            objrec.rec_email = form.cleaned_data['frmrec_email']
            objrec.rec_telefono = form.cleaned_data['frmrec_telefono']
            objrec.rec_calle = form.cleaned_data['frmrec_calle']
            objrec.rec_numero = form.cleaned_data['frmrec_numero']
            objrec.rec_ciudad = form.cleaned_data['frmrec_ciudad']
            objrec.rec_estado = form.cleaned_data['frmrec_estado']
            objrec.rec_codigo_postal = form.cleaned_data['frmrec_codigo_postal']
            objrec.rec_fecha_entrevista = form.cleaned_data[
                'frmrec_fecha_entrevista']
            objrec.rec_fecha_captacion = arrow.now().format('YYYY-MM-DD')
            objrec.rec_proyecto = form.cleaned_data['frmrec_proyecto']
            objrec.rec_proyecto_puesto = form.cleaned_data[
                'frmrec_proyecto_puesto']
            # Recuperar el ID del reclutador para que funcionesn los queries
            # de reporteo
            userID = form.cleaned_data['frmrec_reclutador']
            objrec.rec_reclutador = User.objects.get(username=userID).pk
            objrepo.fecha_registro = arrow.now().format('YYYY-MM-DD')
            objrepo.reclutador = form.cleaned_data['frmrec_reclutador']
            objrepo.como_se_entero = form.cleaned_data['frmrec_comunicacion']
            objrepo.punto_reclutamiento = form.cleaned_data[
                'frmrec_puntoreclutamiento']

            try:
                objrec.save()
                objrepo.save()
                messages.success(request, 'Candidato registrado')
                return HttpResponseRedirect(
                    'reclutadormain.html')
            except (RuntimeError, TypeError, NameError):
                messages.warning(request, 'No se registro el candidato')
                return HttpResponseRedirect('reclutadormain.html')
        else:
            messages.warning(request, 'Errores en los datos, revise la forma')
            return HttpResponseRedirect(
                'registroreclutador.html?proyecto=1')
    else:
        # Usuario logeado
        currentuser = request.user
        # Recpuperamos el ID del proyecto de la solicitud GET
        proyectoid = request.GET['proyecto']
        # Buscamos la info del proyecto segun el ID = PK
        proyectodata = models.Proyecto.objects.get(pk=proyectoid)
        proyectopuesto = models.Puesto.objects.filter(
            puesto_proyecto=proyectoid)
        form = RegistroReclutado()

    return render(request, 'sitio_reclutador/registroreclutador.html', {
        'usuario': currentuser,
        'proyectoID': proyectoid,
        'proyectoDATA': proyectodata,
        'proyectoPUESTO': proyectopuesto,
        'form': form,
        'marca': 'Plataforma Electronica de Reclutamiento',
        'form_id': 'registroreclutador'})


@login_required(login_url='/login/')
def minuevacasa(request):
    ''' Seleccion y busqueda del video unico de cada proyecto, para ser
        mostrado en la pagina Mi Nueva Casa
    '''
    # Usuario logeado
    currentuser = request.user
    # Recpuperamos el ID del proyecto de la solicitud GET
    proyectoid = request.GET['proyecto']
    # Buscamos la info del proyecto segun el ID = PK
    proyectodata = models.Proyecto.objects.get(pk=proyectoid)
    #info del video
    videoTECMA = proyectodata.proyecto_video.__str__()
    print(videoTECMA)

    return render(request, 'sitio_reclutador/minuevacasa.html', {
        'username': currentuser,
        'proyectoID': proyectoid,
        'proyectoDATA': proyectodata,
        'marca': 'Plataforma Electronica de Reclutamiento',
        'videoTECMAfx': videoTECMA
        })


@login_required(login_url='/login/')
def mifamiliatecma(request):
    ''' Localizar el video de eventos y enviarlo a la pagina de Mi Familia
        Tecma.
    '''
    # Usuario logeado
    currentuser = request.user
    # Recpuperamos el ID del proyecto de la solicitud GET
    proyectoid = request.GET['proyecto']
    # Buscamos la info del proyecto segun el ID = PK
    proyectodata = models.Proyecto.objects.get(pk=proyectoid)
    # Buscar info del video segun la categoria
    videoTECMA = models.RecursosVideo.objects.get(
        recursosvideo_nombre='videoTecmaEvent').recursosvideo_archivo_fx

    return render(request, 'sitio_reclutador/mifamiliatecma.html', {
        'username': currentuser,
        'proyectoID': proyectoid,
        'proyectoDATA': proyectodata,
        'marca': 'Plataforma Electronica de Reclutamiento',
        'videoTECMAfx': videoTECMA
        })


@login_required(login_url='/login/')
def mipago(request):
    ''' Informacion de pagos. Identifica los puestos relacionados con el
        proyecto y los regresa en una lista.
    '''

    # Evaluamos si es una solicitud GET o POST
    if request.method == "POST":
        try:
            currentuser = request.user
            puestoid = request.POST.get('selectpuesto', '')
            proyectoid = request.POST.get('proyectoid', '')
            proyectodata = models.Proyecto.objects.get(pk=proyectoid)
            puestoslist = proyectodata.puesto_set.all()
            puesto = models.Puesto.objects.get(pk=puestoid)
            sueldodata = models.Sueldos.objects.get(
                    sueldos_puesto=puestoid)
            sueldototal = str(
                float(sueldodata.sueldos_total_efectivo) +
                float(sueldodata.sueldos_bonos))
            varlist = [
                proyectodata.proyecto_nombre,
                puesto.puesto_nombre,
                sueldodata.sueldos_salario_diario,
                sueldodata.sueldos_bonos,
                sueldodata.sueldos_total_efectivo,
                sueldototal]
            return render(request, 'sitio_reclutador/mipago.html', {
                'username': currentuser,
                'proyectoID': proyectoid,
                'proyectoDATA': proyectodata,
                'marca': 'Plataforma Electronica de Reclutamiento',
                'puestos': puestoslist,
                'sueldosDATA': varlist
                })
        except:
            return render(request, 'sitio_reclutador/mipago.html', {
                'username': currentuser,
                'proyectoID': proyectoid,
                'proyectoDATA': proyectodata,
                'marca': 'Plataforma Electronica de Reclutamiento',
                'puestos': puestoslist,
                'Error': 'No se encontro informacion'
                })

    else:
        # Ususario logeado
        currentuser = request.user
        # recuperar el ID del proyecto
        proyectoid = request.GET['proyecto']
        # Buscamos la info del proyecto segun el ID = PK`
        # a partir del proyecto, tenemos puestos y sueldos
        proyectodata = models.Proyecto.objects.get(pk=proyectoid)
        puestoslist = proyectodata.puesto_set.all()
        print("Sueldos Puestos ==============================================")
        print(puestoslist)

        return render(request, 'sitio_reclutador/mipago.html', {
            'username': currentuser,
            'proyectoID': proyectoid,
            'proyectoDATA': proyectodata,
            'marca': 'Plataforma Electronica de Reclutamiento',
            'puestos': puestoslist
            })


def misprestaciones(request):
    '''Mostrar la lista de prestaciones'''
    # Usuario logeado
    currentuser = request.user
    # Recuperar el ID del proyecto
    proyectoid = request.GET['proyecto']
    # Recuperar el nombre del proyecto
    proyectodata = models.Proyecto.objects.get(pk=proyectoid)
    prestaciones = models.Prestaciones.objects.filter(
        prestaciones_proyecto=proyectoid)

    return render(request, 'sitio_reclutador/misprestaciones.html', {
        'proyectoID': proyectoid,
        'proyecto': proyectodata,
        'prestaciones': prestaciones,
        'marca': 'Plataforma Electronica de Reclutamiento',
        'username': currentuser
        })


@login_required(login_url='/login/')
def milugardetrabajo(request):
    ''' Seccion que regresa la informacion de los mapas paga google maps
    '''
    # Usuario logeado
    currentuser = request.user
    # Recuperar el ID del proyecto
    proyectoid = request.GET['proyecto']
    # Recuperar el nombre del proyecto
    proyectodata = models.Proyecto.objects.get(pk=proyectoid)

    return render(request, 'sitio_reclutador/milugardetrabajo.html', {
        'proyectoID': proyectoid,
        'proyectoNOMBRE': proyectodata.proyecto_nombre,
        'marca': 'Plataforma Electronica de Reclutamiento',
        'username': currentuser
        })


def registrometas(request):
    '''
        Vista para el registro de las metas para el reclutador
    '''
    if request.method == 'POST':
        form = RegistroMetasReclutador(request.POST)
        if form.is_valid():
            rm = form.cleaned_data
            # Instanciar el objeto de metas, esto genera un ID unico
            objrm = models.MetasReclutador()
            # Procesar la forma
            objrm.metas_reclutador_id = rm['frmmetas_reclutador']
            objrm.metas_fecha = rm['frmmetas_fecha']
            objrm.metas_proyecto_id = rm['frmmetas_proyecto']
            objrm.metas_requeridos = rm['frmmetas_requeridos']
            objrm.metas_requeridos_posicion = rm['frmmetas_puesto']
            try:
                objrm.save()
                print("saved")
                messages.success(request, 'Meta registrada')
                return HttpResponseRedirect(
                    'registrometas.html')
            except (RuntimeError, TypeError, NameError):
                messages.warning(request, 'No se completo el registro')
                return HttpResponseRedirect(
                    'registrometas.html')
    else:
        form = RegistroMetasReclutador()
        return render(request, 'sitio_coordinador/registrometas.html', {
            'form': form})


def reportemetas(request):
    '''
    '''
    if request.method == 'POST':
        form = ReporteMetas(request.POST)
    else:
        form = ReporteMetas()
        return render(request, 'sitio_coordinador/reportemetas.html', {
            'form': form})


def ReporteDia(valFecha, valProjecto, valReclutador):
    ''' Funcion que reune la informacion para el reporte '''
    pass