from datetime import datetime
from app.connection import db

class TransaccionProductos(db.Model):
    """
    Clase que representa una transacción de compra de productos realizada por un usuario.

    Atributos:
    - id (int): Identificador único de la transacción. Es una clave primaria.
    - id_usuario (int): ID del usuario que realizó la compra de productos, relacionado con la tabla 'usuario'.
    - total (Decimal): Monto total de la transacción de productos, calculado según los productos comprados.
    - id_metodo_pago (int): ID del método de pago utilizado para la transacción, relacionado con la tabla 'metodo_pago'.
    - fecha_compra (datetime): Fecha y hora en que se realizó la compra de productos. Se establece automáticamente al momento de la creación.
    """
    __tablename__ = 'transaccion_productos'
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    id_metodo_pago = db.Column(db.Integer, db.ForeignKey('metodo_pago.id'), nullable=False)
    fecha_compra = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
