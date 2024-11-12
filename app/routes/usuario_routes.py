from flask import Flask, request, jsonify, session, Blueprint
from app.connection import db
from app.models.usuario import Usuario
from app.models.rol import Rol

usuario_bp = Blueprint('usuario_bp', __name__)

# Ruta para registrar un nuevo usuario
@usuario_bp.route('/registrarse', methods=['POST'])
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
@usuario_bp.route('/login', methods=['POST'])
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
@usuario_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('id_usuario', None)
    return jsonify({"message": "Logout exitoso"}), 200



# Ruta 
