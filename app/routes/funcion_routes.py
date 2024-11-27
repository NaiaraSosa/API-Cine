from flask import Blueprint, request, jsonify
from app.connection import db
from app.models.funcion import Funcion
from app.models.sala import Sala
from app.models.pelicula import Pelicula
from datetime import datetime
from app.routes.usuario_routes import token_required, token_required_admin

funcion_bp = Blueprint('funcion', __name__)

''' Obtener una función por ID '''
@funcion_bp.route('/funciones/<int:id>', methods=['GET'])
@token_required
def obtener_funcion(id, id_usuario):
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


''' Obtener todas las funciones '''
@funcion_bp.route('/funciones', methods=['GET'])
@token_required
def obtener_funciones(id_usuario):
    funciones = Funcion.query.all()
    if not funciones:
        return jsonify({"message": "No hay funciones disponibles"}), 200

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



''' Agregar una función '''
@funcion_bp.route('/funciones', methods=['POST'])
@token_required_admin
def agregar_funcion():
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
    


''' Editar una función por ID '''
@funcion_bp.route('/funciones/<int:id>', methods=['PUT'])
@token_required_admin
def editar_funcion(id):
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
    


''' Eliminar una función por ID '''
@funcion_bp.route('/funciones/<int:id>', methods=['DELETE'])
@token_required_admin
def eliminar_funcion(id):
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
    