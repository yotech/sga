# -*- coding: utf-8 -*-
from gluon import *
from gluon.storage import Storage
from applications.agis.modules import tools
from applications.agis.modules.db import unidad_organica as uo_model
from applications.agis.modules.db import escuela as escuela_model

__doc__ = """Herramientas de GUI para eventos"""

def seleccionar_uo():
    """
    Retorna un grid por medio del cual se puede seleccionar una unidad organica
    el valor del ID seleccionado quedará en:

        request.vars.unidad_organica_id

    el grid para la selección se puede obtener por medio de:

        context.manejo
    """
    uo_model.definir_tabla()
    request = current.request
    response = current.response
    T = current.T
    db = current.db
    if db(uo_model.conjunto()).count() > 1:
        # Si hay más de una UO
        co = CAT()
        header = DIV(T("Seleccionar Unidad Orgánica"), _class="panel-heading")
        body = DIV(_class="panel-body")
        panel = DIV(header, body, _class="panel panel-default")
        # preparar el los campos del grid
        for f in db.unidad_organica:
            f.readable = False
        db.unidad_organica.codigo.readable = True
        db.unidad_organica.nombre.readable = True
        grid = tools.selector(uo_model.conjunto(),
                [db.unidad_organica.codigo,
                 db.unidad_organica.nombre],
                'unidad_organica_id',
            )
        body.append(grid)
        co.append(panel)
        return co
    else:
        # seleccionar la primera y redirecionar a la vista que nos llamo
        if request.vars.keywords:
            request.vars.keywords = ''
        if request.vars.order:
            request.vars.order = ''
        parametros = request.vars
        args=request.args
        parametros.unidad_organica_id = (escuela_model.obtener_sede_central()).id
        u = URL(c=request.controller, f=request.function,
                     vars=parametros, args=args)
        print u
        redirect(u)
        return
