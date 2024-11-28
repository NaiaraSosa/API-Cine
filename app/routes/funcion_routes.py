"""
Archivo: funcion_routes.py
Descripción: Este archivo contiene las rutas relacionadas con las funciones de la aplicación.
Incluye operaciones para obtener, crear, editar y eliminar funciones.
"""

from flask import Blueprint, request, jsonify
from app.connection import db
from app.models.funcion import Funcion
from app.models.sala import Sala
from app.models.pelicula import Pelicula
from datetime import datetime
from app.routes.usuario_routes import token_required, token_required_admin

funcion_bp = Blueprint('funcion', __name__)

@funcion_bp.route('/funciones/<int:id>', methods=['GET'])
@token_required
def obtener_funcion(id, id_usuario):
    """
    Obtener detalles de una función específica por su ID.

    Parámetros de la ruta:
    - id (int): ID de la función.

    Retorna:
    - 200: JSON con los detalles de la función si se encuentra.
    - 404: Mensaje de error si no existe.
    - 500: Mensaje de error si hay problemas con el servidor.
    """
    try:
        funcion = Funcion.query.get(id)

        if not funcion:
            return jsonify({'error': 'La función no se encuentra en el catálogo'}), 404

        funcion_data = {
            'id': funcion.id,
            'id_pelicula': funcion.id_pelicula,
            'id_sala': funcion.id_sala,
            'horario_inicio': funcion.horario_inicio.isoformat() if funcion.horario_inicio else None,
            'horario_fin': funcion.horario_fin.isoformat() if funcion.horario_fin else None,
            'asientos_disponibles': funcion.asientos_disponibles,
            'asientos_totales': funcion.asientos_totales
        }

        return jsonify(funcion_data), 200
    
    except Exception as e:
        return jsonify({'error': f'Error al obtener la función: {str(e)}'}), 500



@funcion_bp.route('/funciones', methods=['GET'])
@token_required
def obtener_funciones(id_usuario):
    """
    Obtener todas las funciones disponibles.

    Retorna:
    - 200: Lista de todas las funciones disponibles en formato JSON. 
    - 400: Mensaje indicando que no hay funciones disponibles.
    - 500: Error interno al procesar la solicitud.
    """
    funciones = Funcion.query.all()
    if not funciones:
        return jsonify({"message": "No hay funciones disponibles"}), 400

    funciones_data = []
    for funcion in funciones:
        funciones_data.append({
            'id': funcion.id,
            'id_pelicula': funcion.id_pelicula,
            'id_sala': funcion.id_sala,
            'horario_inicio': funcion.horario_inicio,
            'horario_fin': funcion.horario_fin,
            'asientos_disponibles': funcion.asientos_disponibles,
            'asientos_totales': funcion.asientos_totales
        })

    return jsonify(funciones_data), 200



@funcion_bp.route('/funciones/pelicula/<int:id>', methods=['GET'])
@token_required 
def obtener_reseñas_pelicula(id, id_usuario):
    """
    Obtener todas las funciones de una película específica.

    Parámetros de la ruta:
    - id (int): ID de la película.

    Requiere:
    - Un token de usuario válido.

    Retorna:
    - 200: Lista de funciones asociadas a la película en formato JSON, incluyendo:
    - 404: Error si la película no existe en la base de datos.
    - 400: Mensaje indicando que no hay funciones disponibles para la película.
    - 500: Error interno al procesar la solicitud.
    """
    pelicula = Pelicula.query.get(id)
    if not pelicula:
        return jsonify({"error": "La película no existe"}), 404
    
    funciones = Funcion.query.filter_by(id_pelicula=id).all()
    if not funciones:
        return jsonify({'message': 'No hay funciones para esta película'}), 400

    funciones_data = []
    for funcion in funciones:
        funciones_data.append({
            'id': funcion.id,
            'id_pelicula': funcion.id_pelicula,
            'id_sala': funcion.id_sala,
            'horario_inicio': funcion.horario_inicio,
            'horario_fin': funcion.horario_fin,
            'asientos_disponibles': funcion.asientos_disponibles,
            'asientos_totales': funcion.asientos_totales
        })

    return jsonify({"funciones": funciones_data}), 200



@funcion_bp.route('/funciones', methods=['POST'])
@token_required_admin
def agregar_funcion():
    """
    Agregar una nueva función al sistema.

    Cuerpo de la solicitud (JSON):
    - id_pelicula (int): ID de la película para la función.
    - id_sala (int): ID de la sala donde se llevará a cabo la función.
    - horario_inicio (str): Fecha y hora de inicio de la función (formato ISO 8601).
    - horario_fin (str): Fecha y hora de fin de la función (formato ISO 8601).

    Retorna:
    - 201: Datos de la función creada.
    - 400: Error si faltan campos requeridos o los datos son inválidos.
    - 404: Error si la película o sala no son válidas.
    - 409: Error si ya existe una función con horario superpuesto en la misma sala.
    - 500: Error interno al guardar la función en la base de datos.
    """
    data = request.get_json()
    id_pelicula = data.get('id_pelicula')
    id_sala = data.get('id_sala')
    horario_inicio = data.get('horario_inicio')
    horario_fin = data.get('horario_fin')

    # Validación de campos requeridos
    if not (id_pelicula and id_sala and horario_inicio and horario_fin is not None):
        return jsonify({"error": "Todos los campos son requeridos"}), 400

    # Validar película
    pelicula = Pelicula.query.get(id_pelicula)
    if not pelicula:
        return jsonify({"error": "Película no válida"}), 404
    
    # Validar sala
    sala = Sala.query.get(id_sala)
    if not sala:
        return jsonify({"error": "Sala no válida"}), 404

    try:
        horario_inicio_dt = datetime.fromisoformat(horario_inicio)
        horario_fin_dt = datetime.fromisoformat(horario_fin)

        # Validar que el horario de inicio no sea en el pasado
        if horario_inicio_dt < datetime.now():
            return jsonify({"error": "El horario de inicio no puede estar en el pasado"}), 400
        
        # Validar que el horario de fin sea posterior al horario de inicio
        if horario_fin_dt <= horario_inicio_dt:
            return jsonify({"error": "El horario de fin debe ser después del horario de inicio"}), 400
    
    except ValueError:
        return jsonify({"error": "Formato de fecha/hora inválido"}), 400

    # Validación de conflictos de horario en la misma sala
    solapamiento = Funcion.query.filter(
        Funcion.id_sala == id_sala,
        Funcion.horario_inicio < horario_fin,
        Funcion.horario_fin > horario_inicio
    ).first()

    if solapamiento:
        return jsonify({"error": "Ya existe una función en esa sala que se solapa con el horario proporcionado"}), 409

    nueva_funcion = Funcion(
        id_pelicula=id_pelicula,
        id_sala=id_sala,
        horario_inicio=horario_inicio_dt,
        horario_fin=horario_fin_dt,
        asientos_disponibles=sala.capacidad,
        asientos_totales=sala.capacidad
    )

    try:
        db.session.add(nueva_funcion)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al agregar la función: {str(e)}"}), 500

    return jsonify({
        "message": "Función creada exitosamente",
        "funcion": {
            "id": nueva_funcion.id,
            "id_pelicula": id_pelicula,
            "id_sala": id_sala,
            "horario_inicio": nueva_funcion.horario_inicio,
            "horario_fin": nueva_funcion.horario_fin,
            "asientos_totales": nueva_funcion.asientos_totales
        }
    }), 201
    


@funcion_bp.route('/funciones/<int:id>', methods=['PUT'])
@token_required_admin
def editar_funcion(id):
    """
    Editar una función existente.

    Parámetros de la ruta:
    - id (int): ID de la función a editar.

    Cuerpo de la solicitud (JSON):
    - id_pelicula (int, opcional): Nuevo ID de la película asociada.
    - id_sala (int, opcional): Nuevo ID de la sala asociada.
    - horario_inicio (str, opcional): Nueva fecha y hora de inicio (formato ISO 8601).
    - horario_fin (str, opcional): Nueva fecha y hora de fin (formato ISO 8601).

    Retorna:
    - 200: Mensaje de éxito y detalles actualizados de la función.
    - 400: Error si los datos proporcionados son inválidos.
    - 404: Error si la función no existe.
    - 409: Error si hay conflictos de horario con otra función en la misma sala.
    - 500: Error interno al actualizar la función.
    """
    data = request.get_json()

    # Buscar la función por ID
    funcion = Funcion.query.get(id)
    if not funcion:
        return jsonify({'error': 'La función no se encuentra en el catálogo'}), 404

    # Obtener nuevos valores o mantener los existentes
    id_pelicula = data.get('id_pelicula', funcion.id_pelicula)
    id_sala = data.get('id_sala', funcion.id_sala)
    horario_inicio = data.get('horario_inicio', funcion.horario_inicio.isoformat() if funcion.horario_inicio else None)
    horario_fin = data.get('horario_fin', funcion.horario_fin.isoformat() if funcion.horario_fin else None)

    if id_pelicula != funcion.id_pelicula:
        pelicula = Pelicula.query.get(id_pelicula)
        if not pelicula:
            return jsonify({"error": "Película no válida"}), 400
    
    sala = Sala.query.get(id_sala)
    if not sala:
        return jsonify({"error": "Sala no válida"}), 400

    # Si la sala cambia, verificar que la capacidad de la nueva sala sea suficiente
    if id_sala != funcion.id_sala:
        asientos_vendidos = funcion.asientos_totales - funcion.asientos_disponibles
        if asientos_vendidos > sala.capacidad:
            return jsonify({"error": "La cantidad de asientos vendidos excede la capacidad de la nueva sala"}), 400
    
    try:
        horario_inicio_dt = datetime.fromisoformat(horario_inicio)
        horario_fin_dt = datetime.fromisoformat(horario_fin)

        # Validar que el horario de inicio no sea en el pasado
        if horario_inicio_dt < datetime.now():
            return jsonify({"error": "El horario de inicio no puede estar en el pasado"}), 400
        
        # Validar que el horario de fin sea posterior al horario de inicio
        if horario_fin_dt <= horario_inicio_dt:
            return jsonify({"error": "El horario de fin debe ser después del horario de inicio"}), 400
    
    except ValueError:
        return jsonify({"error": "Formato de fecha/hora inválido"}), 400

    # Validación de fechas (asegurarse de que el horario_fin sea posterior al horario_inicio)
    if horario_inicio and horario_fin and horario_fin <= horario_inicio:
        return jsonify({"error": "El horario de fin debe ser después del horario de inicio"}), 400

    # Validación de conflictos de horario en la misma sala
    solapamiento = Funcion.query.filter(
        Funcion.id_sala == id_sala,
        Funcion.horario_inicio < horario_fin,
        Funcion.horario_fin > horario_inicio,
        Funcion.id != id  # Excluir la función actual
    ).first()

    if solapamiento:
        return jsonify({"error": "Ya existe una función en esa sala que se solapa con el horario proporcionado"}), 409
    
    # Actualizar los campos
    funcion.id_pelicula = id_pelicula
    funcion.id_sala = id_sala
    funcion.horario_inicio = horario_inicio
    funcion.horario_fin = horario_fin

    # Si no se vendieron entradas, actualizamos los asientos disponibles
    if funcion.asientos_disponibles == funcion.asientos_totales:
        funcion.asientos_totales = sala.capacidad
        funcion.asientos_disponibles = sala.capacidad
    else:
        # Si ya se vendieron entradas, no tocamos los asientos disponibles
        funcion.asientos_totales = sala.capacidad

    try:
        db.session.commit()
        return jsonify({"message": "Función modificada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al modificar la función: {str(e)}"}), 500
    


@funcion_bp.route('/funciones/<int:id>', methods=['DELETE'])
@token_required_admin
def eliminar_funcion(id):
    """
    Eliminar una función por su ID.

    Parámetros de la ruta:
    - id (int): ID de la función a eliminar.

    Retorna:
    - 200: Mensaje confirmando que la función fue eliminada exitosamente.
    - 404: Error si la función no existe en la base de datos.
    - 500: Error interno al eliminar la función de la base de datos.
    """
    funcion = Funcion.query.get(id)

    if not funcion:
        return jsonify({'error': 'La función no se encuentra en el catálogo'}), 404

    try:
        db.session.delete(funcion)
        db.session.commit()
        return jsonify({"message": "Función eliminada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al eliminar la función: {str(e)}"}), 500
    