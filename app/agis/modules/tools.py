#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from gluon import *


def inicializar_administrador():
    db = current.db
    auth = current.auth
    admin_rol = db.auth_group.insert(role='administrators')
    admin_user = db.auth_user.insert(
        email="admin@example.com",
        password=db.auth_user.password.validate('admin')[0],
    )
    db.auth_membership.insert(group_id=admin_rol,user_id=admin_user)
    db.commit()
    auth.login_bare('admin@example.com','admin')

def probar_base_de_datos():
    """Retorna True si la base de datos ya esta inicializada"""
    db = current.db
    if db(db.auth_user.id > 0).count() > 0:
        return True
    # en cc retornar Falso
    return False


def inicializar_base_datos():
    db = current.db
    request = current.request
    # academic regions
    db.region_academica.import_from_csv_file(
        open(os.path.join(request.folder,'db_region_academica.csv'), 'r')
    )
    db.provincia.import_from_csv_file(
        open(os.path.join(request.folder,'db_provincia.csv'), 'r')
    )
    region = db.region_academica[1]
    ihe_id = db.IHE.insert(name='Example University',
        ar_id=region.id,
        classification='10',
        nature='1',
        registration_code='000',
        code='07101000'
    )
    tmp_prov = db.provincia[1]
    db.organic_unit.insert(name='Example Organic Unit',
        province_id=tmp_prov.id,
        aggregation_level='1',
        classification='20',
        registration_code='000',
        IHE_asigg_code='00',
        IHE_id=ihe_id
    )
    db.identity_card_type.bulk_insert([
        {'name': 'Bilhete de Identidade'},
        {'name': 'Pasaporte'},
    ])
    # careers import
    db.career_des.import_from_csv_file(
        open(os.path.join(request.folder,'careers_des.csv'), 'r')
    )
    # regimes import
    db.regime.import_from_csv_file(
        open(os.path.join(request.folder,'db_regime.csv'), 'r')
    )
    # municipality import
    db.municipality.import_from_csv_file(
        open(os.path.join(request.folder,'db_municipality.csv'), 'r')
    )
    # commune import
    db.commune.import_from_csv_file(
        open(os.path.join(request.folder,'db_commune.csv'), 'r')
    )
    # special education needs import
    db.special_education.import_from_csv_file(
        open(os.path.join(request.folder,'db_special_education.csv'), 'r')
    )
    # Middle school types import
    db.middle_school_type.import_from_csv_file(
        open(os.path.join(request.folder,'db_middle_school_type.csv'), 'r')
    )
    # payment concepts
    db.payment_concept.insert(name="Inscripción",
        periodicity=1,
        amount=0.0
    )
