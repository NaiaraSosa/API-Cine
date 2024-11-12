from datetime import datetime
from app.connection import db

class EstadoTransaccion(db.Model):
    __tablename__ = 'estado_transaccion'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)