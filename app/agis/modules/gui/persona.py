# -*- coding: utf-8 -*-
from gluon import *
from gluon.storage import Storage
from applications.agis.modules.db import persona as persona_model

__doc__ = """Herramientas y componentes para el manejo personas"""

def form_editar(uuid):
    """Dado el UUID de una persona retorna el formulario correspondiente para
    la edición de los datos de la misma"""
    persona_model.definir_tabla()
    db = current.db
    T = current.T
    p = persona_model.obtener_por_uuid(uuid)
    title = H3(T("Datos personales"))
    f = SQLFORM(db.persona, p)
    c = CAT(title, DIV(DIV(f, _class="panel-body"),
               _class="panel panel-default"))
    return (c, f)