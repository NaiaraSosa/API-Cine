from flask import Blueprint, request, jsonify
from app.connection import db
from app.models.rol import Rol
from app.routes.usuario_routes import token_required_admin

rol_bp = Blueprint('rol_bp', __name__)

'''Obtener un rol por ID'''
@rol_bp.route('/roles/<int:id>', methods=['GET'])
@token_required_admin  
def obtener_rol(id):
    rol = Rol.query.get(id)
    if not rol:
        return jsonify({'error': 'El rol no se encuentra en el catálogo'}), 404

    rol_data = {
        'id': rol.id,
        'nombre': rol.nombre
    }
    return jsonify(rol_data), 200



'''Obtener todos los roles'''
@rol_bp.route('/roles', methods=['GET'])
@token_required_admin  
def obtener_roles():
    roles = Rol.query.all()
    if not roles:
        return jsonify({"message": "No se encontraron roles en el catálogo"}), 404

    roles_data = [{'id': rol.id, 'nombre': rol.nombre} for rol in roles]
    return jsonify(roles_data), 200



'''Agregar un nuevo rol'''
@rol_bp.route('/roles', methods=['POST'])
@token_required_admin  
def agregar_rol():
    data = request.get_json()
    nombre = data.get('nombre')

    if not nombre:
        return jsonify({"error": "El nombre del rol es requerido"}), 400

    nuevo_rol = Rol(nombre=nombre)

    try:
        db.session.add(nuevo_rol)
        db.session.commit()
        return jsonify({"message": "Rol agregado exitosamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al agregar el rol: {str(e)}"}), 500



'''Editar un rol'''
@rol_bp.route('/roles/<int:id>', methods=['PUT'])
@token_required_admin  
def editar_rol(id):
    rol = Rol.query.get(id)

    if not rol:
        return jsonify({'error': 'El rol no se encuentra en el catálogo'}), 404

    data = request.get_json()
    nombre = data.get('nombre')

    if not nombre:
        return jsonify({'error': 'El nombre del rol es obligatorio'}), 400

    rol.nombre = nombre

    try:
        db.session.commit()
        return jsonify({"message": "Rol modificado exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al modificar el rol: {str(e)}"}), 500



'''Eliminar un rol'''
@rol_bp.route('/roles/<int:id>', methods=['DELETE'])
@token_required_admin  
def eliminar_rol(id):
    rol = Rol.query.get(id)

    if not rol:
        return jsonify({'error': 'El rol no se encuentra en el catálogo'}), 404

    try:
        db.session.delete(rol)
        db.session.commit()
        return jsonify({"message": "Rol eliminado exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al eliminar el rol: {str(e)}"}), 500

