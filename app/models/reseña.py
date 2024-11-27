from datetime import datetime
from app.connection import db

class Reseña(db.Model):
    __tablename__ = 'reseña'
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    id_pelicula = db.Column(db.Integer, db.ForeignKey('pelicula.id'), nullable=False)
    calificacion = db.Column(db.Integer, nullable=False)
    comentario = db.Column(db.String(1000))
    fecha = db.Column(db.DateTime, default=datetime.utcnow) 

    # Relaciones
    usuario = db.relationship("Usuario", backref=db.backref("reseñas", lazy=True))
    pelicula = db.relationship("Pelicula", backref=db.backref("reseñas", lazy=True))