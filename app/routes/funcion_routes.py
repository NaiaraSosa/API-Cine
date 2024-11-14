from flask import Blueprint, request, jsonify
from app.connection import db
from app.models.funcion import Funcion
from app.models.sala import Sala
from app.models.pelicula import Pelicula
from datetime import datetime

funcion_bp = Blueprint('funcion', __name__)

@funcion_bp.route('/agregar_funcion', methods=['POST'])
def agregar_funcion():
    data = request.get_json()
    id_pelicula = data.get('id_pelicula')
    id_sala = data.get('id_sala')
    horario_inicio = data.get('horario_inicio')
    horario_fin = data.get('horario_fin')
    asientos_disponibles = data.get('asientos_disponibles')

    # Validación de campos requeridos
    if not (id_pelicula and id_sala and horario_inicio and horario_fin and asientos_disponibles is not None):
        return jsonify({"error": "Todos los campos son requeridos"}), 400

    # Validación de relación con Pelicula y Sala
    pelicula = Pelicula.query.get(id_pelicula)
    sala = Sala.query.get(id_sala)
    if not pelicula:
        return jsonify({"error": "La película no existe"}), 404
    if not sala:
        return jsonify({"error": "La sala no existe"}), 404

    # Validación de horarios
    try:
        horario_inicio_dt = datetime.fromisoformat(horario_inicio)
        horario_fin_dt = datetime.fromisoformat(horario_fin)
        if horario_fin_dt <= horario_inicio_dt:
            return jsonify({"error": "El horario de fin debe ser después del horario de inicio"}), 400
    except ValueError:
        return jsonify({"error": "Formato de fecha/hora inválido"}), 400
    
    if horario_fin <= horario_inicio:
        return jsonify({"error": "El horario de fin debe ser después del horario de inicio"}), 400

   
    conflicto = Funcion.query.filter(
        Funcion.id_sala == id_sala,
        Funcion.horario_inicio < horario_fin,
        Funcion.horario_fin > horario_inicio
    ).first()

    if conflicto:
        return jsonify({"error": "Ya existe una función en esa sala que se solapa con el horario proporcionado"}), 409



    if asientos_disponibles < 0:
        return jsonify({"error": "Los asientos disponibles deben ser 0 o mayores"}), 400

    nueva_funcion = Funcion(
        id_pelicula=id_pelicula,
        id_sala=id_sala,
        horario_inicio=horario_inicio_dt,
        horario_fin=horario_fin_dt,
        asientos_disponibles=asientos_disponibles
    )

    try:
        db.session.add(nueva_funcion)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al agregar la función: {str(e)}"}), 500

    return jsonify({"message": "Función agregada exitosamente"}), 201


@funcion_bp.route('/eliminar_funcion', methods=['DELETE'])
def eliminar_funcion():
    data = request.get_json()
    id_funcion = data.get('id')

    if not id_funcion:
        return jsonify({"error": "El ID de la función es requerido"}), 400

    funcion = Funcion.query.get(id_funcion)
    if not funcion:
        return jsonify({'error': 'La función no se encuentra en el catálogo'}), 404

    try:
        db.session.delete(funcion)
        db.session.commit()
        return jsonify({"message": "Función eliminada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al eliminar la función: {str(e)}"}), 500
    
    
@funcion_bp.route('/editar_funcion', methods=['PUT'])
def editar_funcion():
    data = request.get_json()
    id_funcion = data.get('id')

    if not id_funcion:
        return jsonify({"error": "El ID de la función es requerido"}), 400

    # Buscar la función por ID
    funcion = Funcion.query.get(id_funcion)
    if not funcion:
        return jsonify({'error': 'La función no se encuentra en el catálogo'}), 404

    # Obtener nuevos valores o mantener los existentes
    id_pelicula = data.get('id_pelicula', funcion.id_pelicula)
    id_sala = data.get('id_sala', funcion.id_sala)
    horario_inicio = data.get('horario_inicio', funcion.horario_inicio.isoformat() if funcion.horario_inicio else None)
    horario_fin = data.get('horario_fin', funcion.horario_fin.isoformat() if funcion.horario_fin else None)
    asientos_disponibles = data.get('asientos_disponibles', funcion.asientos_disponibles)

    # Validar los datos proporcionados
    if not id_pelicula or not id_sala:
        return jsonify({"error": "El ID de la película y la sala son requeridos"}), 400

    try:
        if horario_inicio:
            horario_inicio = datetime.fromisoformat(horario_inicio)
        if horario_fin:
            horario_fin = datetime.fromisoformat(horario_fin)
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido"}), 400

    # Validación de fechas (asegurarse de que el horario_fin sea posterior al horario_inicio)
    if horario_inicio and horario_fin and horario_fin <= horario_inicio:
        return jsonify({"error": "El horario de fin debe ser después del horario de inicio"}), 400

    # Actualizar los campos
    funcion.id_pelicula = id_pelicula
    funcion.id_sala = id_sala
    funcion.horario_inicio = horario_inicio
    funcion.horario_fin = horario_fin
    funcion.asientos_disponibles = asientos_disponibles

    try:
        db.session.commit()
        return jsonify({"message": "Función modificada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al modificar la función: {str(e)}"}), 500