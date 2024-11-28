"""
Archivo: reseña_routes.py
Descripción: Este archivo contiene las rutas relacionadas con las reseñas en la aplicación.
Incluye operaciones para obtener, crear, editar y eliminar reseñas.
"""
from flask import request, jsonify, Blueprint
from app.connection import db
from app.models.reseña import Reseña
from app.models.pelicula import Pelicula
from app.routes.usuario_routes import token_required, token_required_admin

reseña_bp = Blueprint('reseña_bp', __name__)

@reseña_bp.route('/reseñas/<int:id>', methods=['GET'])
@token_required  
def obtener_reseña(id, id_usuario):
    """
    Obtener una reseña por ID.

    Parámetros:
    - id (int): ID único de la reseña.

    Retorna:
    - 200: Detalles de la reseña en formato JSON.
    - 404: Mensaje de error si no se encuentra la reseña.
    """
    reseña = Reseña.query.get(id)
    if not reseña:
        return jsonify({'error': 'Reseña no encontrada'}), 404

    reseña_data = {
        'id': reseña.id,
        'id_usuario': reseña.id_usuario,
        'id_pelicula': reseña.id_pelicula,
        'calificacion': reseña.calificacion,
        'comentario': reseña.comentario,
        'fecha': reseña.fecha
    }

    return jsonify(reseña_data), 200


@reseña_bp.route('/reseñas/pelicula/<int:id>', methods=['GET'])
@token_required 
def obtener_reseñas_pelicula(id, id_usuario):
    """
    Obtener todas las reseñas de una película.

    Parámetros:
    - id (int): ID de la película.

    Retorna:
    - 200: Lista de reseñas en formato JSON.
    - 404: Mensaje de error si no se encuentran reseñas para la película.
    """
    pelicula = Pelicula.query.get(id)
    if not pelicula:
        return jsonify({"error": "La película no existe"}), 404
    
    reseñas = Reseña.query.filter_by(id_pelicula=id).all()
    if not reseñas:
        return jsonify({'message': 'No hay reseñas para esta película'}), 200

    reseñas_data = [{
        "id": reseña.id,
        "id_usuario": reseña.id_usuario,
        "calificacion": reseña.calificacion,
        "comentario": reseña.comentario,
        'fecha': reseña.fecha
    } for reseña in reseñas]

    return jsonify({"reseñas": reseñas_data}), 200


@reseña_bp.route('/reseñas', methods=['POST'])
@token_required 
def agregar_reseña(id_usuario):
    """
    Agregar una nueva reseña.

    Cuerpo de la solicitud:
    - id_pelicula (int): ID de la película.
    - calificacion (int): Calificación de la reseña (entre 1 y 10).
    - comentario (str): Comentario de la reseña.

    Retorna:
    - 201: Mensaje de éxito con detalles de la reseña agregada.
    - 400: Error si falta información requerida o si la calificación no es válida.
    - 500: Error al guardar la reseña en la base de datos.
    """
    data = request.get_json()
    id_pelicula = data.get('id_pelicula')
    calificacion = data.get('calificacion')
    comentario = data.get('comentario')

    if not id_pelicula or calificacion is None:
        return jsonify({'error': 'Faltan datos requeridos: id_usuario, id_pelicula y calificacion'}), 400

    if not (1 <= calificacion <= 10):
        return jsonify({"error": "La calificación debe estar entre 1 y 10"}), 400

    pelicula = Pelicula.query.get(id_pelicula)
    if not pelicula:
        return jsonify({"error": "La película no existe"}), 404

    reseña = Reseña(
        id_usuario=id_usuario,
        id_pelicula=id_pelicula,
        calificacion=calificacion,
        comentario=comentario
    )
    db.session.add(reseña)

    try:
        db.session.commit()
        return jsonify({
            "message": "Reseña agregada exitosamente",
            "reseña": {
                "id": reseña.id,
                "id_pelicula": reseña.id_pelicula,
                "calificacion": reseña.calificacion,
                "comentario": reseña.comentario,
                "fecha": reseña.fecha
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al agregar la reseña: {str(e)}"}), 500


@reseña_bp.route('/reseñas/<int:id>', methods=['PUT'])
@token_required 
def editar_reseña(id, id_usuario):
    """
    Editar una reseña personal.

    Parámetros:
    - id (int): ID de la reseña a modificar.
    
    Cuerpo de la solicitud:
    - calificacion (int): Nueva calificación para la reseña (entre 1 y 10).
    - comentario (str): Nuevo comentario para la reseña.

    Retorna:
    - 200: Mensaje de éxito con los detalles de la reseña modificada.
    - 400: Error si la calificación no es válida.
    - 403: Error si se intenta editar una reseña que no es del usuario.
    - 404: Error si la reseña no existe.
    - 500: Error al guardar los cambios en la base de datos.
    """
    data = request.get_json()
    reseña = Reseña.query.get(id)

    if reseña.id_usuario != id_usuario:
        return jsonify({"error": "No podes editar una reseña que no es tuya"}), 403
    
    if not reseña:
        return jsonify({'error': 'La reseña no existe'}), 404
    
    calificacion = data.get('calificacion', reseña.calificacion)
    comentario = data.get('comentario', reseña.comentario)   

    if calificacion:
        if not (1 <= calificacion <= 10):
            return jsonify({"error": "La calificación debe estar entre 1 y 10"}), 400
        reseña.calificacion = calificacion

    reseña.calificacion = calificacion
    reseña.comentario = comentario

    try:
        db.session.commit()
        return jsonify({
            "message": "Reseña actualizada exitosamente",
            "reseña": {
                "id": reseña.id,
                "id_pelicula": reseña.id_pelicula,
                "calificacion": reseña.calificacion,
                "comentario": reseña.comentario,
                "fecha": reseña.fecha
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al actualizar la reseña: {str(e)}"}), 500


@reseña_bp.route('/reseñas/<int:id>', methods=['DELETE'])
@token_required 
def eliminar_reseña(id, id_usuario):
    """
    Eliminar una reseña personal.

    Parámetros:
    - id (int): ID de la reseña a eliminar.

    Retorna:
    - 200: Mensaje de éxito si la reseña es eliminada.
    - 403: Error si se intenta eliminar una reseña que no es del usuario.
    - 404: Error si la reseña no existe.
    - 500: Error al eliminar la reseña de la base de datos.
    """
    reseña = Reseña.query.get(id)

    if not reseña:
        return jsonify({'error': 'Reseña no encontrada'}), 404

    if reseña.id_usuario != id_usuario:
        return jsonify({"error": "No podes eliminar una reseña que no es tuya"}), 403
    
    try:
        db.session.delete(reseña)
        db.session.commit()
        return jsonify({'message': 'Reseña eliminada exitosamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al eliminar la reseña: {str(e)}'}), 500
