from app.connection import db

class Clasificacion(db.Model):
    """
    Clase que representa una clasificación de una película en la base de datos.

    Atributos:
    - id (int): Identificador único de la clasificación. Es una clave primaria.
    - codigo (str): Código único que identifica la clasificación.
    """
    __tablename__ = 'clasificacion'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), nullable=False)
