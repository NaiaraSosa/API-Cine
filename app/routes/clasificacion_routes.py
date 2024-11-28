"""
Archivo: clasificacion_routes.py
Descripción: Este archivo contiene las rutas relacionadas con las clasificaciones en la aplicación.
Incluye operaciones para obtener, crear, editar y eliminar clasificaciones.
"""

from flask import Blueprint, request, jsonify
from app.connection import db
from app.models.clasificacion import Clasificacion
from app.routes.usuario_routes import token_required_admin

clasificacion_bp = Blueprint('clasificacion_bp', __name__)

@clasificacion_bp.route('/clasificaciones/<int:id>', methods=['GET'])
@token_required_admin
def obtener_clasificacion(id):
    """
    Obtener una clasificación por ID.

    Parámetros:
    - id (int): ID único de la clasificación.

    Retorna:
    - 200: Detalles de la clasificación en formato JSON.
    - 404: Mensaje de error si no se encuentra la clasificación.
    """
    clasificacion = Clasificacion.query.get(id)
    if not clasificacion:
        return jsonify({'error': 'La clasificación no se encuentra en el catálogo'}), 404

    clasificacion_data = {
        'id': clasificacion.id,
        'codigo': clasificacion.codigo
    }

    return jsonify(clasificacion_data), 200



@clasificacion_bp.route('/clasificaciones', methods=['GET'])
@token_required_admin
def obtener_clasificaciones():
    """
    Obtener todas las clasificaciones.

    Retorna:
    - 200: Lista de clasificaciones en formato JSON.
    - 404: Mensaje de error si no se encuentran clasificaciones.
    """
    clasificaciones = Clasificacion.query.all()
    if not clasificaciones:
        return jsonify({"message": "No se encontraron clasificaciones"}), 404

    clasificaciones_data = [{'id': clasificacion.id, 'codigo': clasificacion.codigo} for clasificacion in clasificaciones]
    return jsonify(clasificaciones_data), 200



@clasificacion_bp.route('/clasificaciones', methods=['POST'])
@token_required_admin
def agregar_clasificacion():
    """
    Agregar una nueva clasificación.

    Cuerpo de la solicitud:
    - codigo (str): Código único de la clasificación.

    Retorna:
    - 201: Mensaje de éxito si se agrega la clasificación.
    - 400: Error si no se proporciona el código o si ya existe.
    - 500: Error al guardar la clasificación en la base de datos.
    """
    data = request.get_json()
    codigo = data.get('codigo')

    if not codigo:
        return jsonify({"error": "El código de la clasificación es requerido"}), 400
    
    if Clasificacion.query.filter_by(codigo=codigo).first():
        return jsonify({"error": "El código de la clasificación ya existe"}), 400
    
    nueva_clasificacion = Clasificacion(codigo=codigo)
    
    try:
        db.session.add(nueva_clasificacion)
        db.session.commit()
        return jsonify({"message": "Clasificación agregada exitosamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al agregar la clasificación: {str(e)}"}), 500



@clasificacion_bp.route('/clasificaciones/<int:id>', methods=['PUT'])
@token_required_admin
def editar_clasificacion(id):
    """
    Editar una clasificación por ID.

    Parámetros:
    - id (int): ID único de la clasificación a modificar.

    Cuerpo de la solicitud:
    - codigo (str): Nuevo código para la clasificación.

    Retorna:
    - 200: Mensaje de éxito si se modifica la clasificación.
    - 400: Error si no se proporciona el código o si ya existe.
    - 404: Error si la clasificación no existe.
    - 500: Error al guardar los cambios en la base de datos.
    """
    clasificacion = Clasificacion.query.get(id)

    if not clasificacion:
        return jsonify({'error': 'La clasificación no se encuentra en el catálogo'}), 404

    data = request.get_json()
    codigo = data.get('codigo', clasificacion.codigo)

    if not codigo:
        return jsonify({'error': 'El código de la clasificación es requerido'}), 400

    if codigo != clasificacion.codigo and Clasificacion.query.filter_by(codigo=codigo).first():
        return jsonify({'error': 'El nuevo código de la clasificación ya existe'}), 400
    
    clasificacion.codigo = codigo

    try:
        db.session.commit()
        return jsonify({"message": "Clasificación modificada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al modificar la clasificación: {str(e)}"}), 500



@clasificacion_bp.route('/clasificaciones/<int:id>', methods=['DELETE'])
@token_required_admin
def eliminar_clasificacion(id):
    """
    Eliminar una clasificación por ID.

    Parámetros:
    - id (int): ID único de la clasificación a eliminar.

    Retorna:
    - 200: Mensaje de éxito si se elimina la clasificación.
    - 404: Error si la clasificación no existe.
    - 500: Error al eliminar la clasificación de la base de datos.
    """
    clasificacion = Clasificacion.query.get(id)

    if not clasificacion:
        return jsonify({'error': 'La clasificación no se encuentra en el catálogo'}), 404

    try:
        db.session.delete(clasificacion)
        db.session.commit()
        return jsonify({"message": "Clasificación eliminada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al eliminar la clasificación: {str(e)}"}), 500
