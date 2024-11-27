from app.connection import db

class Entrada(db.Model):
    __tablename__ = 'entrada'
    id = db.Column(db.Integer, primary_key=True)
    id_funcion = db.Column(db.Integer, db.ForeignKey('funcion.id'), nullable=False)
    id_transaccion = db.Column(db.Integer, db.ForeignKey('transaccion_entrada.id'), nullable=False)
