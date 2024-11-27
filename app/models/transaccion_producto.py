from datetime import datetime
from app.connection import db

class TransaccionProductos(db.Model):
    __tablename__ = 'transaccion_productos'
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    id_metodo_pago = db.Column(db.Integer, db.ForeignKey('metodo_pago.id'), nullable=False)
    fecha_compra = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
