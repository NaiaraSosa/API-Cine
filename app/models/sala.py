from app.connection import db

''' Tabla Sala '''
class Sala(db.Model):
    __tablename__ = 'sala'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    capacidad = db.Column(db.Integer, nullable=False) 

