"""
Archivo: sala_routes.py
Descripción: Este archivo contiene las rutas relacionadas con las salas en la aplicación.
Incluye operaciones para obtener, crear, editar y eliminar salas.
"""
from flask import request, jsonify, Blueprint
from app.connection import db
from app.models.sala import Sala
from app.routes.usuario_routes import token_required_admin

sala_bp = Blueprint('sala_bp', __name__)


@sala_bp.route('/salas/<int:id>', methods=['GET'])
@token_required_admin  
def obtener_sala(id):
    """
    Obtiene una sala por su ID.

    Parámetros:
        id (int): El ID de la sala que se desea obtener.

    Retorna:
        - 200: Devuelve los detalles de la sala (id, nombre, capacidad).
        - 404: Si no se encuentra la sala en el catálogo.
    """
    sala = Sala.query.get(id)  
    if not sala:
        return jsonify({'error': 'La sala no se encuentra en el catálogo'}), 404

    sala_data = {
        'id': sala.id,
        'nombre': sala.nombre,
        'capacidad': sala.capacidad,
    }

    return jsonify(sala_data), 200


@sala_bp.route('/salas', methods=['GET'])
@token_required_admin  
def obtener_salas():
    """
    Obtiene una lista de todas las salas disponibles.

    Retorna:
        - 200: Devuelve una lista con los detalles de las salas (id, nombre, capacidad).
        - 404: Si no se encuentran salas en el catálogo.
    """
    salas = Sala.query.all()
    if not salas:
        return jsonify({"message": "No se encontraron salas en el catálogo"}), 404

    salas_data = [{'id': sala.id, 'nombre': sala.nombre, 'capacidad': sala.capacidad} for sala in salas]
    return jsonify(salas_data), 200



'''Agregar una nueva sala'''
@sala_bp.route('/salas', methods=['POST'])
@token_required_admin  
def agregar_sala():
    """
    Agrega una nueva sala al catálogo.

    Cuerpo de la solicitud (JSON):
        - nombre (str): El nombre de la sala.
        - capacidad (int): La capacidad de la sala.

    Retorna:
        - 201: Si la sala fue agregada exitosamente.
        - 400: Si falta algún campo obligatorio o si la sala ya existe.
        - 500: Si ocurre un error al agregar la sala.
    """
    data = request.get_json()
    nombre = data.get('nombre')
    capacidad = data.get('capacidad')

    if not (nombre and capacidad):
        return jsonify({"error": "El nombre y la capacidad son requeridos"}), 400
    
    if Sala.query.filter_by(nombre=nombre).first():
        return jsonify({"error": "La sala ya existe"}), 400
    
    nueva_sala = Sala(
        nombre=nombre,
        capacidad=capacidad,
    )

    try:
        db.session.add(nueva_sala)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al agregar la sala: {str(e)}"}), 500

    return jsonify({"message": "Sala agregada exitosamente"}), 201


@sala_bp.route('/salas/<int:id>', methods=['PUT'])
@token_required_admin  
def editar_sala(id):
    """
    Edita los detalles de una sala existente.

    Parámetros:
        id (int): El ID de la sala a modificar.

    Cuerpo de la solicitud (JSON):
        - nombre (str): El nuevo nombre de la sala (opcional).
        - capacidad (int): La nueva capacidad de la sala (opcional).

    Respuesta:
        - 200: Si la sala fue modificada exitosamente.
        - 404: Si no se encuentra la sala.
        - 400: Si el nombre de la sala ya existe en el catálogo.
        - 500: Si ocurre un error al modificar la sala.
    """
    sala = Sala.query.get(id)

    if not sala:
        return jsonify({'error': 'La sala no se encuentra en el catálogo'}), 404

    data = request.get_json()

    nombre = data.get('nombre', sala.nombre)
    capacidad = data.get('capacidad', sala.capacidad)

    if nombre != sala.nombre and Sala.query.filter_by(nombre=nombre).first():
        return jsonify({"error": "La sala ya existe"}), 400

    sala.nombre = nombre
    sala.capacidad = capacidad

    try:
        db.session.commit()
        return jsonify({"message": "Sala modificada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al modificar la sala: {str(e)}"}), 500
    


@sala_bp.route('/salas/<int:id>', methods=['DELETE'])
@token_required_admin
def eliminar_sala(id):
    """
    Elimina una sala del catálogo.

    Parámetros:
        id (int): El ID de la sala a eliminar.

    Respuesta:
        - 200: Si la sala fue eliminada exitosamente.
        - 404: Si no se encuentra la sala.
        - 500: Si ocurre un error al eliminar la sala.
    """
    sala = Sala.query.get(id)
    if not sala:
        return jsonify({'error': 'La sala no se encuentra en el catálogo'}), 404

    try:
        db.session.delete(sala)
        db.session.commit()
        return jsonify({"message": "Sala eliminada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al eliminar la sala: {str(e)}"}), 500
    
