from app.connection import db

''' Tabla MetodoPago '''
class MetodoPago(db.Model):
    __tablename__ = 'metodo_pago'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)