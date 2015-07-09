# -*- coding: utf-8 -*-
from applications.agis.modules.db import region_academica as ra
from applications.agis.modules.db import descripcion_carrera as db_descripcion_carrera
from applications.agis.modules.db import regimen as tbl_regimen
from applications.agis.modules.db import tipos_ensennanza as tipo_escuela_media
from applications.agis.modules.db import escuela_media as tbl_escuela_media
from applications.agis.modules.db import municipio as tbl_municipio
from applications.agis.modules.db import tipo_documento_identidad as tbl_tipo_dni
from applications.agis.modules.db import discapacidad

sidenav.append(
    [T('Regiones Académicas'), # Titulo del elemento
     URL('region_academica'), # url para el enlace
     ['region_academica'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Descripciones de carrera'), # Titulo del elemento
     URL('descripcion_carrera'), # url para el enlace
     ['descripcion_carrera'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Localidades'), # Titulo del elemento
     URL('localidades'), # url para el enlace
     ['localidades'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Regímenes'), # Titulo del elemento
     URL('regimen'), # url para el enlace
     ['regimen'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Tipos de Enseñanza Media'), # Titulo del elemento
     URL('tipos_ensennaza'), # url para el enlace
     ['tipos_ensennaza'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Escuelas de Enseñanza Media'), # Titulo del elemento
     URL('escuela_media'), # url para el enlace
     ['escuela_media'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Tipos de documento de identidad'), # Titulo del elemento
     URL('tipo_documento_identidad'), # url para el enlace
     ['tipo_documento_identidad'],] # en funciones estará activo este item
)
sidenav.append(
    [T('Necesidades de educación especial'), # Titulo del elemento
     URL('tipo_discapacidad'), # url para el enlace
     ['tipo_discapacidad'],] # en funciones estará activo este item
)



def index():
    redirect(URL('region_academica'))
    return dict(message="hello from general.py",sidenav=sidenav)

@auth.requires_membership('administrators')
def region_academica():
    return dict(sidenav=sidenav,manejo=ra.obtener_manejo())

@auth.requires_membership('administrators')
def descripcion_carrera():
    return dict(sidenav=sidenav,manejo=db_descripcion_carrera.obtener_manejo())

@auth.requires_membership('administrators')
def regimen():
    return dict(sidenav=sidenav,manejo=tbl_regimen.obtener_manejo())

@auth.requires_membership('administrators')
def tipos_ensennaza():
    response.view = "general/regimen.html"
    return dict(sidenav=sidenav,manejo=tipo_escuela_media.obtener_manejo())

@auth.requires_membership('administrators')
def escuela_media():
    return dict(sidenav=sidenav,manejo=tbl_escuela_media.obtener_manejo())

@auth.requires_membership('administrators')
def tipo_documento_identidad():
    return dict(sidenav=sidenav, manejo=tbl_tipo_dni.obtener_manejo())

@auth.requires_membership('administrators')
def tipo_discapacidad():
    return dict(sidenav=sidenav, manejo=discapacidad.obtener_manejo())

@auth.requires_membership('administrators')
def localidades():
    db.provincia.id.readable = False
    db.municipio.id.readable = False
    db.comuna.id.readable = False
    db.municipio.provincia_id.writable = False
    db.comuna.municipio_id.writable = False
    manejo = SQLFORM.smartgrid(db.provincia,
        linked_tables=['municipio','comuna'],showbuttontext=False,details=False,csv=False,
        formstyle='bootstrap',maxtextlength=80,
    )
    return dict(sidenav=sidenav,manejo=manejo)

def obtener_municipios():
    """Cuando es llamado por AJAX retorna la lista de municipios según la provincia"""
    provincia_id = request.vars.provincia_id
    municipios = tbl_municipio.obtener_municipios(provincia_id)
    rs = ''
    for muni in municipios:
        op = OPTION(muni.nombre, _value=muni.id)
        rs += op.xml()
    return rs