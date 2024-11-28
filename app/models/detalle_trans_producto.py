from app.connection import db

class DetalleTransaccionProducto(db.Model):
    """
    Clase que representa los detalles de un producto en una transacción en la base de datos.

    Atributos:
    - id (int): Identificador único del detalle de la transacción. Es una clave primaria.
    - id_transaccion (int): ID de la transacción a la que pertenece este detalle. Es una clave foránea que referencia a la tabla 'transaccion_productos'.
    - id_producto (int): ID del producto involucrado en la transacción. Es una clave foránea que referencia a la tabla 'producto'.
    - cantidad (int): Cantidad de unidades del producto en la transacción.
    - subtotal (decimal): Subtotal de la transacción para este producto. Es el precio total por cantidad de producto.
    """
    __tablename__ = 'detalle_transaccion_producto'
    id = db.Column(db.Integer, primary_key=True)
    id_transaccion = db.Column(db.Integer, db.ForeignKey('transaccion_productos.id'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
