from flask import Flask
from app.connection import db
from app.routes import register_blueprints
import os
import os

def create_app(config_name = None): 
    """
    Crea e inicializa la aplicación Flask con la configuración adecuada.

    Esta función actúa como una fábrica para la aplicación Flask, permitiendo 
    la configuración dinámica según el entorno (desarrollo, pruebas, producción). 
    Carga la configuración de base de datos y rutas, e inicializa la base de datos 
    y los blueprints de la aplicación.

    Parámetros:
        config_name (str): Nombre de la configuración a usar (por ejemplo, 'development', 'testing', etc.). 
                            Si no se especifica, se usa 'development' por defecto.

    Retorna:
        app (Flask): La instancia de la aplicación Flask configurada y lista para usarse.
    """
    app = Flask(__name__)

    # Determina el nombre de la configuración según el entorno
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')  # Usa 'development' si no se especifica

    # Carga la configuración adecuada según el nombre del entorno
    if config_name == 'testing':
        app.config.from_object('app.config.TestingConfig')
    else:
        app.config.from_object('app.config.Config')

    db.init_app(app)

    register_blueprints(app)
    
    # Crear las tablas en la base de datos (solo para testing)
    if config_name == 'testing':
        with app.app_context():
            db.create_all()

    return app
