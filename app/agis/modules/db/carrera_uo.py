#!/usr/bin/env python
# -*- coding: utf-8 -*-
from applications.agis.modules.db import descripcion_carrera
from applications.agis.modules.db import unidad_organica
from applications.agis.modules import tools
from gluon import *

def obtener_por_id(id):
    """ Retorna la carrera y su descripcion """
    db=current.db
    definir_tabla()
    db.carrera_uo.id.readable=False # hide ID field
    return db((db.carrera_uo.id==id) &
              (db.descripcion_carrera.id==db.carrera_uo.descripcion_id)
             ).select().first()

def obtener_selector(unidad_organica_id=None,enlaces_a=[]):
    db = current.db
    definir_tabla()
    if not unidad_organica_id:
        unidad_organica_id = (unidad_organica.obtener_por_escuela())[0].id
    query = ((db.carrera_uo.descripcion_id==db.descripcion_carrera.id) &
            (db.carrera_uo.unidad_organica_id==unidad_organica_id))
    db.carrera_uo.id.readable=False
    return tools.manejo_simple(query, enlaces=enlaces_a, editable=False,
                               buscar=True,campos=[db.descripcion_carrera.nombre,
                                                   db.carrera_uo.id,],
                               orden=[~db.descripcion_carrera.nombre],
                               crear=False,borrar=False)

def carrera_uo_format(fila):
    definir_tabla()
    db = current.db
    return db.descripcion_carrera[fila.descripcion_id].nombre

def obtener_carreras(unidad_organica_id):
    """da el conjunto de carreras de la unidad organica"""
    definir_tabla()
    db = current.db
    filas = db( (db.carrera_uo.unidad_organica_id == unidad_organica_id) &
        (db.carrera_uo.descripcion_id == db.descripcion_carrera.id)
    ).select()
    resultado = []
    for r in filas:
        resultado.append( ( r.carrera_uo.id,r.descripcion_carrera.nombre ) )
    return resultado

def obtener_posibles(unidad_organica_id):
    """
    Retorna una lista de las posibles carreras a agregar a la unidad organica
    """
    definir_tabla()
    db = current.db
    rows = db(db.carrera_uo.unidad_organica_id == None).select(
        db.descripcion_carrera.ALL, db.carrera_uo.ALL,
        orderby=db.descripcion_carrera.nombre,
        left=db.carrera_uo.on((db.descripcion_carrera.id == db.carrera_uo.descripcion_id)
                             &(db.carrera_uo.unidad_organica_id == unidad_organica_id)))
    pos = []
    for item in rows:
        pos.append( (item.descripcion_carrera.id, item.descripcion_carrera.nombre) )
    return pos

def definir_tabla():
    db = current.db
    T = current.T
    descripcion_carrera.definir_tabla()
    unidad_organica.definir_tabla()
    if not hasattr(db, 'carrera_uo'):
        db.define_table('carrera_uo',
            Field( 'descripcion_id','reference descripcion_carrera',required=True ),
            Field( 'unidad_organica_id','reference unidad_organica',required=True ),
            format=carrera_uo_format,
            plural=T( 'Carreras' ),
            singular=T( 'Carrera' ),
        )
        db.carrera_uo.descripcion_id.label=T( 'Descripción de la carrera' )
        db.carrera_uo.unidad_organica_id.label=T( 'Unidad organica' )
        db.commit()