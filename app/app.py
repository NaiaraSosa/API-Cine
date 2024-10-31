import os
from flask import Flask, request, jsonify, session
from dotenv import load_dotenv
from app.connection import db
from .models.usuario import Usuario
from .models.rol import Rol

load_dotenv()

app = Flask(__name__)

# Configuración de SQLAlchemy para conectar con PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa la base
db.init_app(app)

# Crea las tablas si no existen
with app.app_context():
    db.create_all()

@app.get("/")
def home():
    return "Hello World"

# Ruta para registrar un nuevo usuario
@app.route('/registrarse', methods=['POST'])
def registrarse():
    data = request.get_json()
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    correo = data.get('correo_electronico')
    fecha_nac = data.get('fecha_nacimiento')
    contraseña = data.get('contraseña')
    id_rol = data.get('id_rol')

    if not (nombre and apellido and correo and fecha_nac and contraseña and id_rol):
        return jsonify({"error": "Todos los campos son requeridos"}), 400

    # Verifica si el usuario ya existe
    if Usuario.query.filter((Usuario.correo_electronico == correo)).first():
        return jsonify({"error": "El usuario ya existe"}), 409

    # Crea un nuevo usuario
    nuevo_usuario = Usuario(
        nombre=nombre, 
        apellido=apellido, 
        correo_electronico=correo, 
        fecha_nacimiento=fecha_nac,
        id_rol=id_rol)
    nuevo_usuario.set_password(contraseña)
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({"message": "Usuario registrado exitosamente"}), 201

# Ruta para el login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    correo = data.get('correo_electronico')
    contraseña = data.get('contraseña')

    if not (correo and contraseña):
        return jsonify({"error": "Usuario y contraseña requeridos"}), 400

    # Busca el usuario en la base de datos
    usuario = Usuario.query.filter_by(correo_electronico=correo).first()
    if usuario and usuario.check_password(contraseña):
        session['id_usuario'] = usuario.id
        return jsonify({"message": "Login exitoso"}), 200

    return jsonify({"error": "Credenciales inválidas"}), 401

# Ruta para hacer logout
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('id_usuario', None)
    return jsonify({"message": "Logout exitoso"}), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000)




