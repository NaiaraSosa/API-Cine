from app.connection import db

class Configuracion(db.Model):
    """
    Clase que representa una configuración en el sistema, por ejemplo el precio de una entrada.

    Atributos:
    - id (int): Identificador único de la configuración. Es una clave primaria.
    - clave (str): Clave que identifica de forma única la configuración. Debe ser única.
    - valor (str): Valor asociado a la clave de configuración. Puede ser cualquier valor relacionado con la clave.
    """
    __tablename__ = 'configuracion'
    id = db.Column(db.Integer, primary_key=True)
    clave = db.Column(db.String(50), unique=True, nullable=False)  
    valor = db.Column(db.String(100), nullable=False) 
