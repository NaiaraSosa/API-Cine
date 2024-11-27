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
    

    # Validar si el correo ya está registrado
    usuario_existente = Usuario.query.filter_by(correo_electronico=correo).first()
    if usuario_existente:
        return jsonify({"error": "El correo electrónico ya está registrado"}), 409
    
    # Validar y convertir la fecha de nacimiento (MM-DD-YYYY)
    try:
        fecha_nac = datetime.strptime(fecha_nac, "%m-%d-%Y")
    except ValueError:
        return jsonify({"error": "Fecha de nacimiento inválida. Debe ser en formato MM-DD-YYYY"}), 400

    # Validar la contraseña (debe tener entre 6 y 8 caracteres)
    if len(contraseña) < 6 or len(contraseña) > 8:
        return jsonify({"error": "La contraseña debe tener entre 6 y 8 caracteres"}), 400
    
    rol = Rol.query.get(id_rol)
    if not rol:
        return jsonify({"error": "Rol no válido"}), 404

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

    return jsonify({"message": "Usuario registrado exitosamente", "usuario_id": nuevo_usuario.id}), 201



def generate_token(id_usuario, id_rol):
    expiration = datetime.utcnow() + timedelta(minutes=Config.TOKEN_EXPIRATION_MINUTES)
    token = jwt.encode({
        'id_usuario': id_usuario,
        'id_rol': id_rol,
        'exp': expiration
    }, Config.SECRET_KEY, algorithm='HS256')
    return token

def token_required(f):
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Se requiere un token de autorización!'}), 401
        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            id_usuario = data.get('id_usuario')  # Extraer id_usuario del token
            kwargs['id_usuario'] = id_usuario  # Pasar id_usuario a la función decorada
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
        token = generate_token(usuario.id, usuario.id_rol)
        return jsonify({"token": token}), 200
    else: 
        return jsonify({"error": "Credenciales inválidas"}), 401


# Ruta para hacer logout NO PROBADA
@usuario_bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({"message": "Logout exitoso"}), 200



@usuario_bp.route('/usuarios/<int:id>', methods=['GET'])
@token_required
def obtener_usuario(id, id_usuario):
    try:
        usuario = Usuario.query.get(id)  
        if not usuario:
            return jsonify({'error': 'El usuario no se encuentra registrado'}), 404

        usuario_data = {
            'id': usuario.id,
            'nombre': usuario.nombre,
            'apellido': usuario.apellido,
            'correo_electronico': usuario.correo_electronico,
            'fecha_nacimiento': usuario.fecha_nacimiento.strftime('%m-%d-%Y'),  # Asegurando el formato de fecha
            'id_rol': usuario.id_rol
        }

        return jsonify(usuario_data), 200

    except Exception as e:
        return jsonify({'error': f'Error al obtener el usuario: {str(e)}'}), 500
    

@usuario_bp.route('/usuarios', methods=['GET'])
@token_required
def obtener_usuarios(id_usuario):
    try:
        usuarios = Usuario.query.all()  # Obtener todos los usuarios de la base de datos
        if not usuarios:
            return jsonify({'error': 'No hay usuarios registrados'}), 404

        usuarios_data = []
        for usuario in usuarios:
            usuario_data = {
                'id': usuario.id,
                'nombre': usuario.nombre,
                'apellido': usuario.apellido,
                'correo_electronico': usuario.correo_electronico,
                'fecha_nacimiento': usuario.fecha_nacimiento.strftime('%m-%d-%Y'),  # Formato de la fecha
                'id_rol': usuario.id_rol
            }
            usuarios_data.append(usuario_data)

        return jsonify(usuarios_data), 200

    except Exception as e:
        return jsonify({'error': f'Error al obtener los usuarios: {str(e)}'}), 500



@usuario_bp.route('/usuarios/<int:id>', methods=['PUT'])
@token_required
def editar_usuario(id, id_usuario):  
    data = request.get_json()

    # Buscar al usuario por ID
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({'error': 'El usuario no se encuentra registrado'}), 404
    
    if usuario.id != id_usuario:
        return jsonify({"error": "No podes editar un usuario que no es tuyo"}), 403
    
    
    # Actualizar los campos con los datos proporcionados o dejar los actuales
    nombre = data.get('nombre', usuario.nombre)
    apellido = data.get('apellido', usuario.apellido)
    correo = data.get('correo_electronico', usuario.correo_electronico)
    fecha_nac = data.get('fecha_nacimiento', usuario.fecha_nacimiento)
    contraseña = data.get('contraseña', None)  # Si no se proporciona, no se cambia
    id_rol = data.get('id_rol', usuario.id_rol)

    # Verificar si el rol es válido
    if id_rol != usuario.id_rol:
        rol = Rol.query.get(id_rol)
        if not rol:
            return jsonify({"error": "Rol no válido"}), 400
    
        

    # Asignar los valores a las propiedades del usuario
    usuario.nombre = nombre
    usuario.apellido = apellido
    usuario.correo_electronico = correo  

    # Verificar si la fecha de nacimiento llega como string y convertirla
    if isinstance(fecha_nac, str):
        try:
            usuario.fecha_nacimiento = datetime.strptime(fecha_nac, '%m-%d-%Y')
        except ValueError:
            return jsonify({'error': 'Formato de fecha inválido. Usa MM-DD-YYYY'}), 400
    else:
        usuario.fecha_nacimiento = fecha_nac  # Si ya es datetime, simplemente asigna

    usuario.id_rol = id_rol

    # Si se proporciona una nueva contraseña, se debe cifrar y actualizar
    if contraseña:
        if len(contraseña) < 6 or len(contraseña) > 8:
            return jsonify({'error': 'La contraseña debe tener entre 6 y 8 caracteres'}), 400
        usuario.set_password(contraseña)

    # Guardar los cambios en la base de datos
    db.session.commit()

    return jsonify({"message": "Usuario modificado exitosamente"}), 200


@usuario_bp.route('/usuarios/<int:id>', methods=['DELETE'])
@token_required
def eliminar_usuario(id, id_usuario):
    # Buscar al usuario por ID
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({'error': 'El usuario no se encuentra registrado'}), 404

    if usuario.id != id_usuario:
        return jsonify({"error": "No podes eliminar un usuario que no es tuyo"}), 403
    
    # Eliminar el usuario
    db.session.delete(usuario)
    db.session.commit()

    return jsonify({"message": "Usuario eliminado exitosamente"}), 200



