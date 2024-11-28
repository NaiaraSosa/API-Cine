from app.connection import db

class Producto(db.Model):
    """
    Clase que representa un producto en la base de datos.

    Atributos:
    - id (int): Identificador único del producto. Es una clave primaria.
    - nombre (str): Nombre del producto.
    - precio (Decimal): Precio del producto.
    """
    __tablename__ = 'producto'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Numeric(10, 2), nullable=False)