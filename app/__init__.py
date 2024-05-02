import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():

    app = Flask(__name__, template_folder='../web/templates', static_folder='../web/static')

    basedir = os.path.abspath(os.path.dirname(__file__))
    if os.getenv("TEST_ENV"):
        print("Test environment")
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            'sqlite:///' + os.path.join(basedir, '../test-database.db')
    else:
        print("Dev environment")
        app.config['SQLALCHEMY_DATABASE_URI'] = \
            'sqlite:///' + os.path.join(basedir, '../database.db')

    db.init_app(app)
    app.app_context().push()
    db.create_all()

    return app
