from app.connection import db

class DetalleTransaccionProducto(db.Model):
    __tablename__ = 'detalle_transaccion_producto'
    id = db.Column(db.Integer, primary_key=True)
    id_transaccion = db.Column(db.Integer, db.ForeignKey('transaccion_productos.id'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
