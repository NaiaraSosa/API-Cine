from flask import Flask, request, jsonify, session, Blueprint
from app.connection import db
from app.models.pelicula import Pelicula
from app.models.clasificacion import Clasificacion
from app.routes.usuario_routes import token_required, token_required_admin

pelicula_bp = Blueprint('pelicula_bp', __name__)


@pelicula_bp.route('/peliculas', methods=['POST'])
@token_required_admin
def agregar_pelicula():
    data = request.get_json()
    titulo = data.get('titulo')
    director = data.get('director')
    duracion = data.get('duracion')
    id_clasificacion = data.get('id_clasificacion')
    sinopsis = data.get('sinopsis')

    if not (titulo and director and duracion and id_clasificacion and sinopsis):
        return jsonify({"error": "Todos los campos son requeridos"}), 400

    if Pelicula.query.filter((Pelicula.titulo == titulo)).first():
        return jsonify({"error": "La película ya se encuentra en el catálogo."}), 409
    
    clasificacion = Clasificacion.query.get(id_clasificacion)
    if not clasificacion:
        return jsonify({"error": "Clasificación no válida"}), 400

    nueva_pelicula = Pelicula(
        titulo = titulo,
        director = director,
        duracion = duracion,
        id_clasificacion = id_clasificacion,
        sinopsis = sinopsis
    )

    try:
        db.session.add(nueva_pelicula)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al agregar la película: {str(e)}"}), 500

    return jsonify({"message": "Película agregada exitosamente"}), 201


@pelicula_bp.route('/peliculas/<int:id>', methods=['GET'])
@token_required
def obtener_usuario(id):
    pelicula = Pelicula.query.get(id)  
    if not pelicula:
        return jsonify({'error': 'La película no se encuentra en el catálogo'}), 404

    pelicula_data = {
        'id': pelicula.id,
        'titulo': pelicula.titulo,
        'director': pelicula.director,
        'duracion': pelicula.duracion,
        'id_clasificacion': pelicula.id_clasificacion,
        'sinopsis': pelicula.sinopsis
    }

    return jsonify(pelicula_data), 200



@pelicula_bp.route('/peliculas/<int:id>', methods=['PUT'])
@token_required_admin
def editar_pelicula():
    data = request.get_json()

    pelicula = Pelicula.query.get(id)
    if not pelicula:
        return jsonify({'error': 'La película no se encuentra en el catálogo'}), 404

    titulo = data.get('titulo', pelicula.titulo)
    director = data.get('director', pelicula.director)
    duracion = data.get('duracion', pelicula.duracion)
    id_clasificacion = data.get('id_clasificacion', pelicula.id_clasificacion)
    sinopsis = data.get('sinopsis', pelicula.sinopsis)

    if id_clasificacion != pelicula.id_clasificacion:
        clasificacion = Clasificacion.query.get(id_clasificacion)
        if not clasificacion:
            return jsonify({"error": "Clasificación no válida"}), 400

    pelicula.titulo = titulo
    pelicula.director = director
    pelicula.duracion = duracion
    pelicula.id_clasificacion = id_clasificacion
    pelicula.sinopsis = sinopsis

    db.session.commit()

    return jsonify({"message": "Película modificada exitosamente"}), 200



@pelicula_bp.route('/peliculas/<int:id>', methods=['DELETE'])
@token_required_admin
def eliminar_pelicula():
    pelicula = Pelicula.query.get(id)
    if not pelicula:
        return jsonify({'error': 'La película no se encuentra en el catálogo'}), 404

    db.session.delete(pelicula)
    db.session.commit()

    return jsonify({"message": "Película eliminada exitosamente"}), 200