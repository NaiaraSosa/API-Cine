from app.connection import db

class Entrada(db.Model):
    """
    Clase que representa una entrada en la base de datos.

    Atributos:
    - id (int): Identificador único de la entrada. Es una clave primaria.
    - id_funcion (int): ID de la función para la que se compró la entrada. Es una clave foránea que referencia a la tabla 'funcion'.
    - id_transaccion (int): ID de la transacción asociada con la compra de la entrada. Es una clave foránea que referencia a la tabla 'transaccion_entrada'.
    """
    __tablename__ = 'entrada'
    id = db.Column(db.Integer, primary_key=True)
    id_funcion = db.Column(db.Integer, db.ForeignKey('funcion.id'), nullable=False)
    id_transaccion = db.Column(db.Integer, db.ForeignKey('transaccion_entrada.id'), nullable=False)
