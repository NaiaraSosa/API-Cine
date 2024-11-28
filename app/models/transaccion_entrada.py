from datetime import datetime
from app.connection import db


class TransaccionEntrada(db.Model):
    """
    Clase que representa una transacción de compra de entradas a una función de cine realizada por un usuario.

    Atributos:
    - id (int): Identificador único de la transacción. Es una clave primaria.
    - id_usuario (int): ID del usuario que realizó la transacción, relacionado con la tabla 'usuario'.
    - id_funcion (int): ID de la función de cine a la que se adquirieron las entradas, relacionado con la tabla 'funcion'.
    - cantidad_entradas (int): Número de entradas compradas en la transacción.
    - total (Decimal): Monto total de la transacción, calculado según el precio de las entradas.
    - id_metodo_pago (int): ID del método de pago utilizado para la transacción, relacionado con la tabla 'metodo_pago'.
    - fecha (datetime): Fecha y hora en que se realizó la transacción. Se establece automáticamente al momento de la creación.
    """
    __tablename__ = 'transaccion_entrada'
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    id_funcion = db.Column(db.Integer, db.ForeignKey('funcion.id'), nullable=False)
    cantidad_entradas = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    id_metodo_pago = db.Column(db.Integer, db.ForeignKey('metodo_pago.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
