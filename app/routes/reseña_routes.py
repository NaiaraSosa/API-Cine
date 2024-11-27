from flask import Flask, request, jsonify, Blueprint
from app.connection import db
from app.models.reseña import Reseña
from app.routes.usuario_routes import token_required, token_required_admin

reseña_bp = Blueprint('reseña_bp', __name__)

'''Obtener reseña por ID'''
@reseña_bp.route('/reseñas/<int:id>', methods=['GET'])
@token_required  
def obtener_reseña(id):
    reseña = Reseña.query.get(id)
    if not reseña:
        return jsonify({'error': 'Reseña no encontrada'}), 404

    reseña_data = {
        'id': reseña.id,
        'id_usuario': reseña.id_usuario,
        'id_pelicula': reseña.id_pelicula,
        'calificacion': reseña.calificacion,
        'comentario': reseña.comentario,
    }

    return jsonify(reseña_data), 200

'''Obtener todas las reseñas'''
@reseña_bp.route('/reseñas', methods=['GET'])
@token_required 
def obtener_reseñas():
    reseñas = Reseña.query.all()
    if not reseñas:
        return jsonify({'message': 'No hay reseñas disponibles'}), 200

    reseñas_data = []
    for reseña in reseñas:
        reseñas_data.append({
            'id': reseña.id,
            'id_usuario': reseña.id_usuario,
            'id_pelicula': reseña.id_pelicula,
            'calificacion': reseña.calificacion,
            'comentario': reseña.comentario,
        })

    return jsonify(reseñas_data), 200

'''Agregar reseña'''
@reseña_bp.route('/reseñas', methods=['POST'])
@token_required 
def agregar_reseña():
    data = request.get_json()

    id_usuario = data.get('id_usuario')
    id_pelicula = data.get('id_pelicula')
    calificacion = data.get('calificacion')
    comentario = data.get('comentario')

    if not (id_usuario and id_pelicula and calificacion):
        return jsonify({'error': 'Faltan datos requeridos: id_usuario, id_pelicula y calificacion'}), 400

    nueva_reseña = Reseña(
        id_usuario=id_usuario,
        id_pelicula=id_pelicula,
        calificacion=calificacion,
        comentario=comentario
    )

    try:
        db.session.add(nueva_reseña)
        db.session.commit()
        return jsonify({'message': 'Reseña agregada exitosamente', 'id': nueva_reseña.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al agregar la reseña: {str(e)}'}), 500

'''Editar reseña'''
@reseña_bp.route('/reseñas/<int:id>', methods=['PUT'])
@token_required 
def editar_reseña(id):
    reseña = Reseña.query.get(id)

    if not reseña:
        return jsonify({'error': 'Reseña no encontrada'}), 404

    data = request.get_json()

    calificacion = data.get('calificacion', reseña.calificacion)
    comentario = data.get('comentario', reseña.comentario)

    reseña.calificacion = calificacion
    reseña.comentario = comentario

    try:
        db.session.commit()
        return jsonify({'message': 'Reseña actualizada exitosamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al actualizar la reseña: {str(e)}'}), 500

'''Eliminar reseña'''
@reseña_bp.route('/reseñas/<int:id>', methods=['DELETE'])
@token_required_admin 
def eliminar_reseña(id):
    reseña = Reseña.query.get(id)
    if not reseña:
        return jsonify({'error': 'Reseña no encontrada'}), 404

    try:
        db.session.delete(reseña)
        db.session.commit()
        return jsonify({'message': 'Reseña eliminada exitosamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al eliminar la reseña: {str(e)}'}), 500