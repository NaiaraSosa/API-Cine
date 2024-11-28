from app.connection import db

class Sala(db.Model):
    """
    Clase que representa una sala en la base de datos.

    Atributos:
    - id (int): Identificador único de la sala. Es una clave primaria.
    - nombre (str): Nombre de la sala.
    - capacidad (int): Número máximo de personas que la sala puede albergar.
    """
    __tablename__ = 'sala'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    capacidad = db.Column(db.Integer, nullable=False) 

