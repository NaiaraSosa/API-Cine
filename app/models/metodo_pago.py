from app.connection import db

class MetodoPago(db.Model):
    """
    Clase que representa un método de pago en la base de datos.

    Atributos:
    - id (int): Identificador único del método de pago. Es una clave primaria.
    - tipo (str): Tipo de método de pago.
    """
    __tablename__ = 'metodo_pago'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)