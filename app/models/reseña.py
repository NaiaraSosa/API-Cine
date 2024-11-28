from datetime import datetime
from app.connection import db

class Reseña(db.Model):
    """
    Clase que representa una reseña de una película realizada por un usuario.

    Atributos:
    - id (int): Identificador único de la reseña. Es una clave primaria.
    - id_usuario (int): ID del usuario que realizó la reseña, relacionado con la tabla 'usuario'.
    - id_pelicula (int): ID de la película que se reseña, relacionado con la tabla 'pelicula'.
    - calificacion (int): Calificación de la película dada por el usuario.
    - comentario (str): Comentario opcional del usuario sobre la película.
    - fecha (datetime): Fecha y hora en que la reseña fue escrita. Se establece automáticamente al momento de la creación.
    """
    __tablename__ = 'reseña'
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    id_pelicula = db.Column(db.Integer, db.ForeignKey('pelicula.id'), nullable=False)
    calificacion = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.String(1000))
    fecha = db.Column(db.DateTime, default=datetime.utcnow) 

