from flask import request, jsonify, session, Blueprint
from psycopg2 import IntegrityError
from app.connection import db
from app.models.usuario import Usuario
from app.models.rol import Rol
import jwt
from datetime import datetime, timedelta
from app.config import Config

usuario_bp = Blueprint('usuario_bp', __name__)

@usuario_bp.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    correo = data.get('correo_electronico')
    fecha_nac = data.get('fecha_nacimiento')
    contraseña = data.get('contraseña')
    id_rol = data.get('id_rol')

    if not (nombre and apellido and correo and fecha_nac and contraseña and id_rol):
        return jsonify({"error": "Todos los campos son requeridos"}), 400

    rol = Rol.query.get(id_rol)
    if not rol:
        return jsonify({"error": "Rol no válido"}), 400

    nuevo_usuario = Usuario(
        nombre=nombre, 
        apellido=apellido, 
        correo_electronico=correo, 
        fecha_nacimiento=fecha_nac,
        id_rol=id_rol)
    nuevo_usuario.set_password(contraseña)
    
    try:
        db.session.add(nuevo_usuario)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "El correo electrónico ya está registrado"}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al registrar el usuario: {str(e)}"}), 500

    return jsonify({"message": "Usuario registrado exitosamente"}), 201



def generate_token(username, id_rol):
    expiration = datetime.utcnow() + timedelta(minutes=30)
    token = jwt.encode({
        'username': username,
        'id_rol': id_rol,
        'exp': expiration
    }, Config.SECRET_KEY, algorithm='HS256')
    return token

def token_required(f):
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Falta el token!'}), 401
        try:
            jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'El token ha expirado'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido'}), 403
        return f(*args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated


def token_required_admin(f):
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Falta el token!'}), 401
        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            id_rol = data['id_rol']
            if id_rol != 1:
                return jsonify({'message': 'Usuario no autorizado.'}), 403
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'El token ha expirado'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido'}), 403
        return f(*args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated

@usuario_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    correo = data.get('correo_electronico', '').strip()
    contraseña = data.get('contraseña')

    if not (correo and contraseña):
        return jsonify({"error": "Usuario y contraseña requeridos"}), 400

    usuario = Usuario.query.filter_by(correo_electronico=correo).first()
    if usuario and usuario.check_password(contraseña):
        token = generate_token(correo, usuario.id_rol)
        return jsonify({"token": token}), 200
    else: 
        return jsonify({"error": "Credenciales inválidas"}), 401



# Ruta para hacer logout (mejor usar GET en lugar de POST)
@usuario_bp.route('/logout', methods=['GET'])  # Cambié a GET
def logout():
    session.pop('id_usuario', None)
    return jsonify({"message": "Logout exitoso"}), 200

# Ruta para obtener un usuario
@usuario_bp.route('/usuarios/<int:id>', methods=['GET'])
@token_required_admin
def obtener_usuario(id):
    usuario = Usuario.query.get(id)  
    if not usuario:
        return jsonify({'error': 'El usuario no se encuentra registrado'}), 404

    usuario_data = {
        'id': usuario.id,
        'nombre': usuario.nombre,
        'apellido': usuario.apellido,
        'correo_electronico': usuario.correo_electronico,
        'fecha_nacimiento': usuario.fecha_nacimiento,
        'id_rol': usuario.id_rol
    }

    return jsonify(usuario_data), 200

# Ruta para editar un usuario
@usuario_bp.route('/usuarios/<int:id>', methods=['PUT'])  # Corregí el parámetro 'id'
@token_required_admin
def editar_usuario(id):  # Agregué 'id' como parámetro
    data = request.get_json()

    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({'error': 'El usuario no se encuentra registrado'}), 404
    
    nombre = data.get('nombre', usuario.nombre)
    apellido = data.get('apellido', usuario.apellido)
    correo = data.get('correo_electronico', usuario.correo_electronico)
    fecha_nac = data.get('fecha_nacimiento', usuario.fecha_nacimiento)
    contraseña = data.get('contraseña', usuario.contraseña)
    id_rol = data.get('id_rol', usuario.id_rol)

    if id_rol != usuario.id_rol:
        rol = Rol.query.get(id_rol)
        if not rol:
            return jsonify({"error": "Rol no válido"}), 400

    usuario.nombre = nombre
    usuario.apellido = apellido
    usuario.correo_electronico = correo  # Corregí el nombre de la propiedad
    usuario.fecha_nacimiento = fecha_nac  # Corregí el nombre de la propiedad
    usuario.id_rol = id_rol

    # Solo actualiza la contraseña si se pasa un nuevo valor
    nueva_contraseña = data.get('contraseña')
    if nueva_contraseña:
        usuario.set_password(nueva_contraseña)

    db.session.commit()

    return jsonify({"message": "Usuario modificado exitosamente"}), 200

# Ruta para eliminar un usuario
@usuario_bp.route('/usuarios/<int:id>', methods=['DELETE'])  # Corregí la ruta de 'ususarios' a 'usuarios'
@token_required_admin
def eliminar_usuario(id):  # Agregué 'id' como parámetro
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({'error': 'El usuario no se encuentra registrado'}), 404

    db.session.delete(usuario)
    db.session.commit()

    return jsonify({"message": "Usuario eliminado exitosamente"}), 200

@usuario_bp.route('/usuarios', methods=['GET'])
@token_required_admin  # Si quieres proteger la ruta para que solo un administrador pueda acceder
def obtener_usuarios():
    """Obtener todos los usuarios"""
    usuarios = Usuario.query.all()
    if not usuarios:
        return jsonify({'error': 'No hay usuarios registrados'}), 404

    # Formateamos los datos de cada usuario
    usuarios_data = []
    for usuario in usuarios:
        usuarios_data.append({
            'id': usuario.id,
            'nombre': usuario.nombre,
            'apellido': usuario.apellido,
            'correo_electronico': usuario.correo_electronico,
            'fecha_nacimiento': usuario.fecha_nacimiento,
            'id_rol': usuario.id_rol
        })

    return jsonify(usuarios_data), 200



