from flask import request, jsonify, Blueprint
from app.connection import db
from app.models.sala import Sala
from app.routes.usuario_routes import token_required_admin

sala_bp = Blueprint('sala_bp', __name__)


'''Obtener sala por ID'''
@sala_bp.route('/salas/<int:id>', methods=['GET'])
@token_required_admin  
def obtener_sala(id):
    sala = Sala.query.get(id)  
    if not sala:
        return jsonify({'error': 'La sala no se encuentra en el catálogo'}), 404

    sala_data = {
        'id': sala.id,
        'nombre': sala.nombre,
        'capacidad': sala.capacidad,
    }

    return jsonify(sala_data), 200



'''Obtener todas las salas'''
@sala_bp.route('/salas', methods=['GET'])
@token_required_admin  
def obtener_salas():
    salas = Sala.query.all()
    if not salas:
        return jsonify({"message": "No se encontraron salas en el catálogo"}), 404

    salas_data = [{'id': sala.id, 'nombre': sala.nombre, 'capacidad': sala.capacidad} for sala in salas]
    return jsonify(salas_data), 200



'''Agregar una nueva sala'''
@sala_bp.route('/salas', methods=['POST'])
@token_required_admin  
def agregar_sala():
    data = request.get_json()
    nombre = data.get('nombre')
    capacidad = data.get('capacidad')

    if not (nombre and capacidad):
        return jsonify({"error": "El nombre y la capacidad son requeridos"}), 400
    
    if Sala.query.filter_by(nombre=nombre).first():
        return jsonify({"error": "La sala ya existe"}), 400
    
    nueva_sala = Sala(
        nombre=nombre,
        capacidad=capacidad,
    )

    try:
        db.session.add(nueva_sala)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al agregar la sala: {str(e)}"}), 500

    return jsonify({"message": "Sala agregada exitosamente"}), 201



'''Editar una sala'''
@sala_bp.route('/salas/<int:id>', methods=['PUT'])
@token_required_admin  # Protege este endpoint si es necesario
def editar_sala(id):
    sala = Sala.query.get(id)

    if not sala:
        return jsonify({'error': 'La sala no se encuentra en el catálogo'}), 404

    data = request.get_json()

    nombre = data.get('nombre', sala.nombre)
    capacidad = data.get('capacidad', sala.capacidad)

    if nombre != sala.nombre and Sala.query.filter_by(nombre=nombre).first():
        return jsonify({"error": "La sala ya existe"}), 400

    sala.nombre = nombre
    sala.capacidad = capacidad

    try:
        db.session.commit()
        return jsonify({"message": "Sala modificada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al modificar la sala: {str(e)}"}), 500
    


'''Eliminar una sala'''
@sala_bp.route('/salas/<int:id>', methods=['DELETE'])
@token_required_admin
def eliminar_sala(id):
    sala = Sala.query.get(id)
    if not sala:
        return jsonify({'error': 'La sala no se encuentra en el catálogo'}), 404

    try:
        db.session.delete(sala)
        db.session.commit()
        return jsonify({"message": "Sala eliminada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al eliminar la sala: {str(e)}"}), 500
    
