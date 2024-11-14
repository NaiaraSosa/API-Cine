from flask import Flask, request, jsonify, session, Blueprint
from app.connection import db
from app.models.sala import Sala

sala_bp = Blueprint('sala_bp', __name__)

@sala_bp.route('/agregar_sala', methods=['POST'])
def agregar_sala():
    data = request.get_json()
    nombre = data.get('nombre')
    capacidad = data.get('capacidad')

    if not (nombre and capacidad):
        return jsonify({"error": "El nombre y la capacidad de la sala son requeridos"}), 400

    
    if capacidad <= 0:
        return jsonify({"error": "La capacidad debe ser mayor a 0"}), 400

    if Sala.query.filter_by(nombre=nombre).first():
        return jsonify({"error": "La sala ya existe"}), 409

    nueva_sala = Sala(
        nombre=nombre,
        capacidad=capacidad
    )

    try:
        db.session.add(nueva_sala)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al agregar la sala: {str(e)}"}), 500

    return jsonify({"message": "Sala agregada exitosamente"}), 201


@sala_bp.route('/eliminar_sala', methods=['DELETE'])
def eliminar_sala():
    # Obtener el ID de la sala desde el cuerpo de la solicitud
    data = request.get_json()
    id_sala = data.get('id')

    # Verificar que el ID esté presente
    if not id_sala:
        return jsonify({"error": "El ID de la sala es requerido"}), 400

    # Buscar la sala por ID
    sala = Sala.query.get(id_sala)
    if not sala:
        return jsonify({'error': 'La sala no se encuentra en el catálogo'}), 404

    try:
        # Eliminar las funciones asociadas si no se usa cascada
        for funcion in sala.funciones:
            db.session.delete(funcion)

        # Eliminar la sala
        db.session.delete(sala)
        db.session.commit()
        return jsonify({"message": "Sala eliminada exitosamente, incluidas sus funciones"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al eliminar la sala: {str(e)}"}), 500

sala_bp = Blueprint('sala_bp', __name__)

@sala_bp.route('/editar_sala', methods=['PUT'])
def editar_sala():
    data = request.get_json()
    id_sala = data.get('id')

    if not id_sala:
        return jsonify({"error": "El ID de la sala es requerido"}), 400

    sala = Sala.query.get(id_sala)
    if not sala:
        return jsonify({'error': 'La sala no se encuentra en el catálogo'}), 404

    nombre = data.get('nombre', sala.nombre)
    capacidad = data.get('capacidad', sala.capacidad)

    if capacidad <= 0:
        return jsonify({"error": "La capacidad debe ser mayor que 0"}), 400

    sala.nombre = nombre
    sala.capacidad = capacidad

    try:
        db.session.commit()
        return jsonify({"message": "Sala modificada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al modificar la sala: {str(e)}"}), 500