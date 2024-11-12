from app.connection import db

class Funcion(db.Model):
    __tablename__ = 'funcion'
    id = db.Column(db.Integer, primary_key=True)
    id_pelicula = db.Column(db.Integer, db.ForeignKey('pelicula.id'), nullable=False)
    id_sala = db.Column(db.Integer, db.ForeignKey('sala.id'), nullable=False)
    horario_inicio = db.Column(db.DateTime, nullable=False) 
    horario_fin = db.Column(db.DateTime, nullable=False)  
    asientos_disponibles = db.Column(db.Integer, nullable=False, default=0) 

    # Relaciones
    pelicula = db.relationship("Pelicula", backref=db.backref("funciones", lazy=True))
    sala = db.relationship("Sala", backref=db.backref("funciones", lazy=True))