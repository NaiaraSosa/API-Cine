from app.connection import db

class Rol(db.Model):
    """
    Clase que representa un rol de usuario en la base de datos.

    Atributos:
    - id (int): Identificador único del rol. Es una clave primaria.
    - nombre (str): Nombre del rol.
    """
    __tablename__ = 'rol'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)