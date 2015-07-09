# -*- coding: utf-8 -*-

from applications.agis.modules import tools
from applications.agis.modules.db import escuela
from applications.agis.modules.db import unidad_organica
from applications.agis.modules.db import regimen_uo
from applications.agis.modules.db import carrera_uo
from applications.agis.modules.db import ano_academico as a_academico
from applications.agis.modules.db import departamento as dpto
from applications.agis.modules.db import nivel_academico as nivel
from applications.agis.modules.db import asignatura
from applications.agis.modules.db import plan_curricular
from applications.agis.modules.db import plazas
from applications.agis.modules.db import evento
from applications.agis.modules.db import asignatura_plan
from applications.agis.modules.db import grupo

sidenav.append(
    [T('Escuela'), # Titulo del elemento
     URL('configurar_escuela'), # url para el enlace
     ['configurar_escuela'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Unidades organicas'), # Titulo del elemento
     URL('gestion_uo'), # url para el enlace
     ['gestion_uo'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Régimen a realizar en la UO'), # Titulo del elemento
     URL('asignar_regimen'), # url para el enlace
     ['asignar_regimen'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Carreras a impartir en las UO'), # Titulo del elemento
     URL('asignar_carrera'), # url para el enlace
     ['asignar_carrera'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Gestión de Años Académicos'), # Titulo del elemento
     URL('ano_academico'), # url para el enlace
     ['ano_academico'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Departamentos'), # Titulo del elemento
     URL('departamentos'), # url para el enlace
     ['departamentos'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Niveles Académicos'), # Titulo del elemento
     URL('nivel_academico'), # url para el enlace
     ['nivel_academico'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Asignaturas'), # Titulo del elemento
     URL('asignaturas'), # url para el enlace
     ['asignaturas'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Grupos de estudiantes'), # Titulo del elemento
     URL('grupos'), # url para el enlace
     ['grupos'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Planes Curriculares'), # Titulo del elemento
     URL('planes_curriculares'), # url para el enlace
     ['planes_curriculares','asignatura_por_plan'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Plazas a otorgar'), # Titulo del elemento
     URL('plazas_estudiantes'), # url para el enlace
     ['plazas_estudiantes'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Eventos'), # Titulo del elemento
     URL('eventos'), # url para el enlace
     ['eventos'],] # en funciones estará activo este item
)

def index():
    redirect(URL('configurar_escuela'))
    return dict(message="hello from instituto.py")

@auth.requires_membership('administrators')
def grupos():
    manejo = grupo.obtener_manejo()
    #TODO: mantener chequeado con los cambios
    response.view="instituto/nivel_academico.html"
    return dict( sidenav=sidenav,manejo=manejo )

@auth.requires_membership('administrators')
def plazas_estudiantes_ajax():
    if request.ajax:
        c_id = int(request.vars.c)
        a_id = int(request.vars.a)
        r_id = int(request.vars.r)
        p = plazas.buscar_plazas(ano_academico_id=a_id,
                                 regimen_id=r_id,
                                 carrera_id=c_id)
        db.plazas.id.readable=False
        db.plazas.ano_academico_id.default = a_id
        db.plazas.ano_academico_id.readable=False
        db.plazas.ano_academico_id.writable=False
        db.plazas.regimen_id.default = r_id
        db.plazas.regimen_id.readable = False
        db.plazas.regimen_id.writable = False
        db.plazas.carrera_id.default = c_id
        db.plazas.carrera_id.readable = False
        db.plazas.carrera_id.writable = False
        if not p:
            db.plazas.insert()
            db.commit()
            p = plazas.buscar_plazas(ano_academico_id=a_id,
                                     regimen_id=r_id,
                                     carrera_id=c_id)
        form = SQLFORM(db.plazas,record=p,formstyle="divs")
        if form.process().accepted:
            response.flash = T('Cambios guardados')
        return dict(form=form)
    else:
        raise HTTP(500)

@auth.requires_membership('administrators')
def plazas_estudiantes():
    def enlaces_step2(fila):
        return A(T('Definir plazas para nuevos ingresos'),
                 _href=URL('instituto',
                           'plazas_estudiantes',
                           vars=dict(step=2,carrera_id=fila.carrera_uo.id)),
                 _class='btn btn-link')
    if not 'step' in request.vars:
        redirect(URL('plazas_estudiantes',vars=dict(step=1)))
    step=request.vars.step
    manejo = None
    if step=='1':
        manejo=carrera_uo.obtener_selector(
            enlaces_a=[dict(header='',body=enlaces_step2)])
    elif step=='2':
        # mostrar por cada año academico los regimenes de la unidad organica
        # de la carrera seleccionada.
        carrera=carrera_uo.obtener_por_id(int(request.vars.carrera_id))
        a_academicos = db((db.ano_academico.id>0) &
                          (db.evento.ano_academico_id==db.ano_academico.id) &
                          ((db.evento.tipo=='1') & (db.evento.estado==True))
                         ).select(db.ano_academico.id,db.ano_academico.nombre)
        regimenes = regimen_uo.obtener_regimenes_por_unidad( carrera.carrera_uo.unidad_organica_id )
        return dict(sidenav=sidenav,
                    carrera=carrera,
                    step=step,
                    a_academicos=a_academicos,
                    regimenes=regimenes)
        pass

    return dict( sidenav=sidenav,manejo=manejo,step=step )

@auth.requires_membership('administrators')
def nivel_academico():
    manejo = nivel.obtener_manejo()
    return dict( sidenav=sidenav,manejo=manejo )

@auth.requires_membership('administrators')
def ano_academico():
    manejo = a_academico.obtener_manejo()
    return dict( sidenav=sidenav,manejo=manejo )

@auth.requires_membership('administrators')
def asignaturas():
    manejo = asignatura.obtener_manejo()
    return dict( sidenav=sidenav,manejo=manejo )

@auth.requires_membership('administrators')
def asignatura_por_plan():
    if 'plan_id' in request.vars:
        plan_id=int(request.vars.plan_id)
    else:
        raise HTTP( 404 )
    manejo=asignatura_plan.obtener_manejo( plan_id )
    response.view = "instituto/asignaturas.html"
    return dict( sidenav=sidenav,manejo=manejo )

@auth.requires_membership('administrators')
def planes_curriculares():
    enlaces=[ dict(header='',body=lambda fila:A( T('Gestionar'),_href=URL('asignatura_por_plan',vars=dict(plan_id=fila.id)) )) ]
    manejo = plan_curricular.obtener_manejo(enlaces)
    response.view = "instituto/asignaturas.html"
    return dict( sidenav=sidenav,manejo=manejo )

@auth.requires_membership('administrators')
def eventos():
    manejo = evento.obtener_manejo()
    response.view = "instituto/asignaturas.html"
    return dict( sidenav=sidenav,manejo=manejo )

@auth.requires_membership('administrators')
def departamentos():
    manejo = dpto.obtener_manejo()
    return dict( sidenav=sidenav,manejo=manejo )

@auth.requires_membership('administrators')
def configurar_escuela():
    """Presenta formulario con los datos de la escuela y su sede cetral"""
    instituto = escuela.obtener_escuela()
    db.escuela.id.readable = False
    db.escuela.id.writable = False

    form_escuela = SQLFORM( db.escuela,instituto,formstyle='bootstrap' )
    response.title = T("Configurar escuela")
    if form_escuela.process(dbio=False).accepted:
        form_escuela.vars.codigo=escuela.calcular_codigo_escuela( db.escuela._filter_fields( form_escuela.vars ) )
        db( db.escuela.id==instituto.id ).update( **db.escuela._filter_fields( form_escuela.vars ) )
        db.commit()
        unidad_organica.actualizar_codigos()
        session.flash = T( "Cambios guardados" )
        redirect('configurar_escuela')
    return dict(form_escuela=form_escuela,sidenav=sidenav)

@auth.requires_membership('administrators')
def asignar_carrera():
    """
    Permite asignarle carreras a las unidades organicas
    """
    esc = escuela.obtener_escuela()
    select_uo = unidad_organica.widget_selector(escuela_id=esc.id)
    if 'unidad_organica_id' in request.vars:
        unidad_organica_id = int(request.vars.unidad_organica_id)
    else:
        unidad_organica_id = escuela.obtener_sede_central().id
    db.carrera_uo.unidad_organica_id.default = unidad_organica_id
    db.carrera_uo.unidad_organica_id.writable = False
    db.carrera_uo.unidad_organica_id.readable = False
    db.carrera_uo.id.readable = False
    db.carrera_uo.id.writable = False
    query = ( db.carrera_uo.unidad_organica_id == unidad_organica_id )
    if 'new' in request.args:
        # preparar para agregar un nuevo elemento
        posibles_carreras = carrera_uo.obtener_posibles(unidad_organica_id)
        if posibles_carreras:
            db.carrera_uo.descripcion_id.requires = IS_IN_SET( posibles_carreras, zero=None )
        else:
            session.flash = T("Ya se han asociados todas las posibles carreras a la UO")
            redirect(URL('asignar_carrera',vars={'unidad_organica_id': unidad_organica_id}))
    manejo = tools.manejo_simple( query,editable=False )
    return dict( sidenav=sidenav, select_uo=select_uo, manejo=manejo )

@auth.requires_membership('administrators')
def asignar_regimen():
    esc = escuela.obtener_escuela()
    select_uo = unidad_organica.widget_selector(escuela_id=esc.id)
    if 'unidad_organica_id' in request.vars:
        unidad_organica_id = int(request.vars.unidad_organica_id)
    else:
        unidad_organica_id = escuela.obtener_sede_central().id
    db.regimen_unidad_organica.unidad_organica_id.default = unidad_organica_id
    db.regimen_unidad_organica.unidad_organica_id.writable = False
    db.regimen_unidad_organica.id.readable = False
    query = (db.regimen_unidad_organica.unidad_organica_id ==  unidad_organica_id)
    if 'new' in request.args:
        # preparar para agregar un nuevo elemento
        posibles_regimenes = regimen_uo.obtener_posibles_en_instituto(unidad_organica_id)
        if posibles_regimenes:
            db.regimen_unidad_organica.regimen_id.requires = IS_IN_SET( posibles_regimenes, zero=None )
        else:
            session.flash = T("Ya se han asociados todos los posibles regímenes a la UO")
            redirect(URL('asignar_regimen',vars={'unidad_organica_id': unidad_organica_id}))
    manejo = tools.manejo_simple(query,editable=False)
    return dict(sidenav=sidenav,manejo=manejo,select_uo=select_uo)

@auth.requires_membership('administrators')
def gestion_uo():
    """Vista para la gestión de las unidades organicas"""
    esc = escuela.obtener_escuela()
    manejo = unidad_organica.obtener_manejo(esc.id)
    return dict(manejo=manejo,sidenav=sidenav)