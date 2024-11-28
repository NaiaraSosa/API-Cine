"""
Archivo: pelicula_routes.py
Descripción: Este archivo contiene las rutas relacionadas con las películas en la aplicación.
Incluye operaciones para obtener, crear, editar y eliminar métodos de pago.
"""
from flask import request, jsonify, Blueprint
from app.connection import db
from app.models.pelicula import Pelicula
from app.models.clasificacion import Clasificacion
from app.routes.usuario_routes import token_required, token_required_admin

pelicula_bp = Blueprint('pelicula_bp', __name__)


@pelicula_bp.route('/peliculas/<int:id>', methods=['GET'])
@token_required
def obtener_pelicula(id, id_usuario):
    """
    Obtener los detalles de una película por su ID.

    Parámetros:
    id (int): El ID de la película a obtener.

    Retorna:
    - 200: Detalles de la película en formato JSON.
    - 404: Mensaje de error si no se encuentra la película.
    """
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



@pelicula_bp.route('/peliculas', methods=['GET'])
@token_required
def obtener_peliculas(id_usuario):
    """
    Obtener todas las películas.

    Retorna:
    - 200: Lista de películas en formato JSON.
    - 404: Mensaje de error si no se encuentran películas.
    """
    peliculas = Pelicula.query.all()

    if not peliculas:
        return jsonify({"message": "No hay películas en el catálogo"}), 200

    peliculas_data = []
    for pelicula in peliculas:
        peliculas_data.append({
        'id': pelicula.id,
        'titulo': pelicula.titulo,
        'director': pelicula.director,
        'duracion': pelicula.duracion,
        'id_clasificacion': pelicula.id_clasificacion,
        'sinopsis': pelicula.sinopsis
        })
    return jsonify(peliculas_data), 200



@pelicula_bp.route('/peliculas', methods=['POST'])
@token_required_admin
def agregar_pelicula():
    """
    Agregar una nueva película.

    Cuerpo de la solicitud:
    - titulo (str): Título de la película.
    - director (str): Director de la película.
    - duracion (int): Duración de la película en minutos.
    - id_clasificacion (int): ID de la clasificación de la película.
    - sinopsis (str): Sinopsis de la película.

    Retorna:
    - 201: Mensaje de éxito si se agrega la película.
    - 400: Error si faltan campos requeridos.
    - 409: Error si la película ya existe.
    - 500: Error al guardar la película en la base de datos.
    """
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



@pelicula_bp.route('/peliculas/<int:id>', methods=['PUT'])
@token_required_admin
def editar_pelicula(id):
    """
    Editar una película por ID.

    Parámetros:
    - id (int): ID de la película a modificar.

    Cuerpo de la solicitud:
    - titulo (str): Nuevo título para la película.
    - director (str): Nuevo director para la película.
    - duracion (int): Nueva duración de la película en minutos.
    - id_clasificacion (int): Nuevo ID de clasificación para la película.
    - sinopsis (str): Nueva sinopsis para la película.

    Retorna:
    - 200: Mensaje de éxito si se modifica la película.
    - 400: Error si no se proporciona un campo requerido o la clasificación no es válida.
    - 404: Error si la película no existe.
    - 500: Error al guardar los cambios en la base de datos.
    """
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
def eliminar_pelicula(id):
    """
    Eliminar una película por ID.

    Parámetros:
    - id (int): ID de la película a eliminar.

    Retorna:
    - 200: Mensaje de éxito si se elimina la película.
    - 404: Error si la película no existe.
    - 500: Error al eliminar la película de la base de datos.
    """
    pelicula = Pelicula.query.get(id)
    if not pelicula:
        return jsonify({'error': 'La película no se encuentra en el catálogo'}), 404

    db.session.delete(pelicula)
    db.session.commit()

    return jsonify({"message": "Película eliminada exitosamente"}), 200
