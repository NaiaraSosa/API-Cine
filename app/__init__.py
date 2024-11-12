from flask import Flask
from app.connection import db
from app.routes import register_blueprints
#from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config') 
    db.init_app(app)

    # Registrar Blueprints
    register_blueprints(app)

    with app.app_context():
        db.create_all()  

    return app

