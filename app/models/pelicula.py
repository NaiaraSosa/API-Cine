from app.connection import db

class Pelicula(db.Model):
    """
    Clase que representa una película en la base de datos.

    Atributos:
    - id (int): Identificador único de la película. Es una clave primaria.
    - titulo (str): Título de la película.
    - director (str): Nombre del director de la película.
    - duracion (int): Duración de la película en minutos.
    - id_clasificacion (int): ID de la clasificación de la película, relacionado con la tabla 'clasificacion'.
    - sinopsis (str): Descripción breve de la trama de la película.
    """
    __tablename__ = 'pelicula'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)  
    director = db.Column(db.String(100), nullable=False) 
    duracion = db.Column(db.Integer, nullable=False) 
    id_clasificacion = db.Column(db.Integer, db.ForeignKey('clasificacion.id'), nullable=False)
    sinopsis = db.Column(db.String(1000))  
