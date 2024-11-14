from flask import Flask, request, jsonify, session, Blueprint
from psycopg2 import IntegrityError
from app.connection import db
from app.models.usuario import Usuario
from app.models.rol import Rol

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



@usuario_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    correo = data.get('correo_electronico', '').strip()
    contraseña = data.get('contraseña')

    if not (correo and contraseña):
        return jsonify({"error": "Usuario y contraseña requeridos"}), 400

    usuario = Usuario.query.filter_by(correo_electronico=correo).first()
    if usuario and usuario.check_password(contraseña):
        session['id_usuario'] = usuario.id
        session.permanent = True
        return jsonify({"message": "Login exitoso"}), 200

    return jsonify({"error": "Credenciales inválidas"}), 401



# Ruta para hacer logout NO PROBADA
@usuario_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('id_usuario', None)
    return jsonify({"message": "Logout exitoso"}), 200



# Ruta NO PROBADA
@usuario_bp.route('/usuarios/<int:id>', methods=['GET'])
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




# Ruta NO PROBADA
@usuario_bp.route('/usuarios/<int:id>', methods=['PUT'])
def editar_usuario():
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
    usuario.correo = correo
    usuario.fecha_nac = fecha_nac
    usuario.contraseña = contraseña
    usuario.id_rol = id_rol

    nueva_contraseña = data.get('contraseña')
    if nueva_contraseña:
        usuario.set_password(nueva_contraseña)

    db.session.commit()

    return jsonify({"message": "Usuario modificado exitosamente"}), 200



# Ruta NO PROBADA
@usuario_bp.route('/ususarios/<int:id>', methods=['DELETE'])
def eliminar_usuario():
    usuario = Usuario.query.get(id)
    if not usuario:
        return jsonify({'error': 'El usuario no se encuentra registrado'}), 404

    db.session.delete(usuario)
    db.session.commit()

    return jsonify({"message": "Película eliminada exitosamente"}), 200


