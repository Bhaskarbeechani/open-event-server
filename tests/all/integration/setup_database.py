import os
import sys

import logging

from app.instance import current_app as app
from app.models import db
from app.models.setting import Environment
from app.settings import set_settings

_basedir = os.path.abspath(os.path.dirname(__file__))


class Setup(object):
    @staticmethod
    def create_app():
        app.config.from_object('config.TestingConfig')
        app.secret_key = 'super secret key'
        app.logger.addHandler(logging.StreamHandler(sys.stdout))
        app.logger.setLevel(logging.ERROR)
        with app.test_request_context():
            db.create_all()
            set_settings(secret='super secret key', app_name='Open Event', app_environment=Environment.TESTING)

        return app

    @staticmethod
    def drop_db():
        with app.test_request_context():
            db.session.remove()
            if app.config['SQLALCHEMY_DATABASE_URI'].find('postgresql://') > -1:
                # drop_all has problems with foreign keys in postgres database (cyclic dependency)
                db.engine.execute("drop schema if exists public cascade")
                db.engine.execute("create schema public")
            else:
                # drop all works for SQLite and should work for other DBMS like MySQL, Mongo etc
                db.drop_all()
