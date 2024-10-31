from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.connection import db


class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    correo_electronico = db.Column(db.String(120), unique=True, nullable=False)
    fecha_nacimiento = db.Column(db.DateTime, default=datetime.utcnow)
    contraseña = db.Column(db.String(128), nullable=False)
    id_rol = db.Column(db.Integer, db.ForeignKey('rol.id'), nullable=False)
    fecha_registro = db.Column(db.Date, default=datetime.utcnow)

    def set_password(self, contraseña):
        self.contraseña = generate_password_hash(contraseña)

    def check_password(self, contraseña):
        return check_password_hash(self.contraseña, contraseña)
