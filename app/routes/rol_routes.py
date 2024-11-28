"""
Archivo: rol_routes.py
Descripción: Este archivo contiene las rutas relacionadas con los roles en la aplicación.
Incluye operaciones para obtener, crear, editar y eliminar roles.
"""

from flask import Blueprint, request, jsonify
from app.connection import db
from app.models.rol import Rol
from app.routes.usuario_routes import token_required_admin

rol_bp = Blueprint('rol_bp', __name__)

@rol_bp.route('/roles/<int:id>', methods=['GET'])
@token_required_admin  
def obtener_rol(id):
    """
        Obtener un rol por ID.

        Parámetros:
        - id (int): ID único del rol.

        Retorna:
        - 200: Detalles del rol en formato JSON.
        - 404: Mensaje de error si no se encuentra el rol.
        """
    rol = Rol.query.get(id)
    if not rol:
        return jsonify({'error': 'El rol no se encuentra en el catálogo'}), 404

    rol_data = {
        'id': rol.id,
        'nombre': rol.nombre
    }
    return jsonify(rol_data), 200



@rol_bp.route('/roles', methods=['GET'])
@token_required_admin  
def obtener_roles():
    """
        Obtener todos los roles.

        Retorna:
        - 200: Lista de roles en formato JSON.
        - 404: Mensaje de error si no hay roles en el catálogo.
        """
    roles = Rol.query.all()
    if not roles:
        return jsonify({"message": "No se encontraron roles en el catálogo"}), 404

    roles_data = [{'id': rol.id, 'nombre': rol.nombre} for rol in roles]
    return jsonify(roles_data), 200



@rol_bp.route('/roles', methods=['POST'])
@token_required_admin  
def agregar_rol():
    """
        Agregar un nuevo rol.

        Cuerpo de la solicitud:
        - nombre (str): Nombre del rol.

        Retorna:
        - 201: Mensaje de éxito si se agrega el rol.
        - 400: Error si no se proporciona el nombre del rol.
        - 500: Error al guardar el rol en la base de datos.
        """
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
    """
        Editar un rol.

        Parámetros:
        - id (int): ID del rol a modificar.

        Cuerpo de la solicitud:
        - nombre (str): Nuevo nombre para el rol.

        Retorna:
        - 200: Mensaje de éxito si se modifica el rol.
        - 400: Error si no se proporciona el nombre del rol.
        - 404: Error si el rol no existe.
        - 500: Error al guardar los cambios.
        """
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



@rol_bp.route('/roles/<int:id>', methods=['DELETE'])
@token_required_admin 
def eliminar_rol(id):
    """
        Eliminar un rol.

        Parámetros:
        - id (int): ID del rol a eliminar.

        Retorna:
        - 200: Mensaje de éxito si se elimina el rol.
        - 404: Error si el rol no existe.
        - 500: Error al eliminar el rol de la base de datos.
        """
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

