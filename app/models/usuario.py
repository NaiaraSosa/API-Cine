from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.connection import db

class Usuario(db.Model):
    """
    Clase que representa a un usuario en la base de datos.

    Atributos:
    - id (int): Identificador único del usuario. Es una clave primaria.
    - nombre (str): Nombre del usuario.
    - apellido (str): Apellido del usuario.
    - correo_electronico (str): Correo electrónico del usuario. Debe ser único.
    - fecha_nacimiento (datetime): Fecha de nacimiento del usuario.
    - id_rol (int): ID que representa el rol del usuario, relacionado con la tabla Rol.
    - contraseña_hash (str): Contraseña del usuario, almacenada como hash para mayor seguridad.

    Métodos:
    - set_password(contraseña): Método para establecer la contraseña del usuario.
    - check_password(contraseña): Método para verificar si la contraseña ingresada es correcta.
    """
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    correo_electronico = db.Column(db.String(120), unique=True, nullable=False)
    fecha_nacimiento = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    contraseña = db.Column(db.String(120), nullable=False)
    id_rol = db.Column(db.Integer, db.ForeignKey('rol.id'), nullable=False)
    fecha_registro = db.Column(db.Date, default=datetime.utcnow)

    def set_password(self, contraseña):
        """
        Establece el hash de la contraseña del usuario.

        Parámetro:
        - contraseña (str): La contraseña a ser hasheada.
        """
        if len(contraseña) < 6 or len(contraseña) > 8:
            raise ValueError("La contraseña debe tener entre 6 y 8 caracteres.")
        self.contraseña = generate_password_hash(contraseña)

    def check_password(self, contraseña):
        """
        Verifica si la contraseña proporcionada coincide con el hash almacenado.

        Parámetro:
        - contraseña (str): La contraseña a verificar.

        Retorna:
        - bool: True si la contraseña es válida, False de lo contrario.
        """
        return check_password_hash(self.contraseña, contraseña)
