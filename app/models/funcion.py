from app.connection import db

class Funcion(db.Model):
    """
    Clase que representa una función de cine en la base de datos.

    Atributos:
    - id (int): Identificador único de la función. Es una clave primaria.
    - id_pelicula (int): ID de la película proyectada en la función. Es una clave foránea que referencia a la tabla 'pelicula'.
    - id_sala (int): ID de la sala donde se realiza la función. Es una clave foránea que referencia a la tabla 'sala'.
    - horario_inicio (datetime): Fecha y hora de inicio de la función.
    - horario_fin (datetime): Fecha y hora de finalización de la función.
    - asientos_disponibles (int): Número de asientos disponibles para la función.
    - asientos_totales (int): Número total de asientos en la sala de la función.
    """
    __tablename__ = 'funcion'
    id = db.Column(db.Integer, primary_key=True)
    id_pelicula = db.Column(db.Integer, db.ForeignKey('pelicula.id'), nullable=False)
    id_sala = db.Column(db.Integer, db.ForeignKey('sala.id'), nullable=False)
    horario_inicio = db.Column(db.DateTime, nullable=False) 
    horario_fin = db.Column(db.DateTime, nullable=False)  
    asientos_disponibles = db.Column(db.Integer, nullable=False) 
    asientos_totales = db.Column(db.Integer, nullable=False)
