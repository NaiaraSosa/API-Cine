"""
Archivo: usuario_routes.py
Descripción: Este archivo contiene las rutas relacionadas con los usuarios en la aplicación. 
Incluye operaciones para crear, obtener y autenticar usuarios, así como para gestionar 
tokens de autenticación JWT, y proporcionar acceso a la información de los usuarios de manera segura.

Decoradores:
- token_required: Verifica que el usuario esté autenticado mediante un token JWT.
- token_required_admin: Verifica que el usuario tenga un rol de administrador.
"""
from flask import request, jsonify, Blueprint
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
    """
    Crear un nuevo usuario.

    Cuerpo de la solicitud:
    - nombre (str): Nombre del usuario.
    - apellido (str): Apellido del usuario.
    - correo_electronico (str): Correo electrónico del usuario.
    - fecha_nacimiento (str): Fecha de nacimiento del usuario (formato MM-DD-YYYY).
    - contraseña (str): Contraseña del usuario (entre 6 y 8 caracteres).
    - id_rol (int): ID del rol del usuario.

    Retorna:
    - 201: Mensaje de éxito si el usuario se registra correctamente.
    - 400: Error si falta algún campo obligatorio o si hay un problema con los datos.
    - 409: Error si el correo electrónico ya está registrado.
    - 500: Error al registrar el usuario.
    """
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
    """
    Generar un token JWT para un usuario.

    Parámetros:
    - id_usuario (int): ID del usuario.
    - id_rol (int): ID del rol del usuario.

    Retorna:
    - token (str): Token JWT generado.
    """
    expiration = datetime.utcnow() + timedelta(minutes=Config.TOKEN_EXPIRATION_MINUTES)
    token = jwt.encode({
        'id_usuario': id_usuario,
        'id_rol': id_rol,
        'exp': expiration
    }, Config.SECRET_KEY, algorithm='HS256')
    return token

def token_required(f):
    """
    Decorador que valida el token de autorización para acceso a rutas protegidas.

    Retorna:
    - 401: Si no se proporciona un token.
    - 403: Si el token es inválido o ha expirado.
    - Ejecuta la función original si el token es válido.
    """
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
    """
    Decorador que valida el token de autorización y verifica que el usuario tenga rol de administrador.

    Retorna:
    - 401: Si no se proporciona un token.
    - 403: Si el token es inválido, ha expirado o el rol del usuario no es administrador.
    - Ejecuta la función original si el token es válido y el usuario es administrador.
    """
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
    """
    Iniciar sesión para un usuario y generar un token JWT.

    Cuerpo de la solicitud:
    - correo_electronico (str): Correo electrónico del usuario.
    - contraseña (str): Contraseña del usuario.

    Retorna:
    - 200: Token JWT si las credenciales son correctas.
    - 400: Error si falta algún campo obligatorio.
    - 401: Error si las credenciales son inválidas.
    """
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
    

@usuario_bp.route('/usuarios/<int:id>', methods=['GET'])
@token_required
def obtener_usuario(id, id_usuario):
    """
    Obtener información de un usuario por su ID.

    Parámetros:
    - id (int): ID del usuario a obtener.

    Retorna:
    - 200: Detalles del usuario en formato JSON.
    - 404: Error si el usuario no existe.
    - 500: Error al obtener el usuario.
    """
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
    """
    Obtener todos los usuarios registrados.

    Retorna:
    - 200: Lista de usuarios en formato JSON.
    - 404: Error si no hay usuarios registrados.
    - 500: Error al obtener los usuarios.
    """
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
    """
    Editar los detalles de un usuario existente.

    Parámetros:
    - id (int): ID del usuario a editar.
    - id_usuario (int): ID del usuario que hace la solicitud (para asegurar que no edite a otro usuario).

    Cuerpo de la solicitud:
    - nombre (str, opcional): Nombre del usuario.
    - apellido (str, opcional): Apellido del usuario.
    - correo_electronico (str, opcional): Correo electrónico del usuario.
    - fecha_nacimiento (str, opcional): Fecha de nacimiento del usuario (formato MM-DD-YYYY).
    - contraseña (str, opcional): Nueva contraseña del usuario (entre 6 y 8 caracteres).
    - id_rol (int, opcional): ID del rol del usuario.

    Retorna:
    - 200: Mensaje de éxito si el usuario es editado correctamente.
    - 400: Error si los datos son inválidos o faltan.
    - 403: Error si el usuario intenta editar a otro usuario.
    - 404: Error si el usuario no se encuentra registrado.
    - 500: Error al editar el usuario.
    """
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
    """
    Eliminar un usuario de la base de datos.

    Parámetros:
    - id (int): ID del usuario a eliminar.
    - id_usuario (int): ID del usuario que realiza la solicitud (para asegurar que no elimine a otro usuario).

    Retorna:
    - 200: Mensaje de éxito si el usuario es eliminado correctamente.
    - 403: Error si el usuario intenta eliminar a otro usuario.
    - 404: Error si el usuario no se encuentra registrado.
    - 500: Error al eliminar el usuario.
    """
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



