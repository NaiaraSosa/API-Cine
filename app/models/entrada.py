from app.connection import db

''' Tabla Entrada '''
class Entrada(db.Model):
    __tablename__ = 'entrada'
    id = db.Column(db.Integer, primary_key=True)
    id_funcion = db.Column(db.Integer, db.ForeignKey('funcion.id'), nullable=False)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False) 
    id_metodo_pago = db.Column(db.Integer, db.ForeignKey('metodo_pago.id'))
