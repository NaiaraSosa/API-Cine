from flask import Flask
from app.connection import db
from app.routes import register_blueprints
import os

''' Inicialización de la API '''
def create_app(config_name=None):
    app = Flask(__name__)

    # Determina el nombre de la configuración según el entorno
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')  # Usa 'development' si no se especifica

    # Carga la configuración adecuada según el nombre del entorno
    if config_name == 'testing':
        app.config.from_object('app.config.TestingConfig')
    else:
        app.config.from_object('app.config.Config')

    # Inicializa la base de datos
    db.init_app(app)

    # Registrar los blueprints de las rutas
    register_blueprints(app)

    # Crear las tablas en la base de datos (solo para testing)
    if config_name == 'testing':
        with app.app_context():
            db.create_all()

    return app

