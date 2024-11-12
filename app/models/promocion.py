from app.connection import db
from datetime import datetime

class Promocion(db.Model):
    __tablename__ = 'promocion'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(1000), nullable=False)
    fecha_inicio = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)