"""Módulo de funcionalidad de DB"""
import mariadb
from flask import current_app, g
# from flask.cli import with_appcontext


def get_db():
    """Retornar el conector y cursor a la DB"""
    if 'db' not in g:
        g.db = mariadb.connect(
            host=current_app.config['DATABASE_HOST'],
            user=current_app.config['DATABASE_USER'],
            password=current_app.config['DATABASE_PASSWORD'],
            database=current_app.config['DATABASE']
        )
        g.c = g.db.cursor(dictionary=True)
    return g.db, g.c


def close_db(e=None):
    """Cerrar DB"""
    db = g.pop('db', None)

    if db is not None:
        db.close()
