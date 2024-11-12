from flask import Flask, request, jsonify, session, Blueprint
from app.connection import db
from app.models.pelicula import Pelicula
from app.models.clasificacion import Clasificacion

pelicula_bp = Blueprint('peliculas_bp', __name__)

@pelicula_bp.route('/agregar_pelicula', methods=['POST'])
def agregar_pelicula():
    data = request.get_json()
    titulo = data.get('titulo')
    director = data.get('director')
    duracion = data.get('duracion')
    id_clasificacion = data.get('id_clasificacion')
    sinopsis = data.get('sinopsis')

    if not (titulo and director and duracion and sinopsis):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    # Verifica si el usuario ya existe
    if Pelicula.query.filter((Pelicula.titulo == titulo)).first():
        return jsonify({"error": "La película ya se encuentra en el catálogo."}), 409

    # Crea un nuevo usuario
    nueva_pelicula = Pelicula(
        titulo = titulo,
        director = director,
        duracion = duracion,
        id_clasificacion = id_clasificacion,
        sinopsis = sinopsis
    )
    db.session.add(nueva_pelicula)
    db.session.commit()

    return jsonify({"message": "Película agregada exitosamente"}), 201