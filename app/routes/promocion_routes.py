from flask import Blueprint, request, jsonify
from app.connection import db
from app.models.promocion import Promocion
from datetime import datetime
from app.routes.usuario_routes import token_required, token_required_admin

promocion_bp = Blueprint('promocion_bp', __name__)

'''obtener promocion'''
@promocion_bp.route('/promociones/<int:id>', methods=['GET'])
@token_required_admin  
def obtener_promocion(id):
    promocion = Promocion.query.get(id)  
    if not promocion:
        return jsonify({'error': 'La promoción no se encuentra en el catálogo'}), 404

    promocion_data = {
        'id': promocion.id,
        'descripcion': promocion.descripcion,
        'fecha_inicio': promocion.fecha_inicio.isoformat(),
        'fecha_fin': promocion.fecha_fin.isoformat()
    }

    return jsonify(promocion_data), 200

# Agregar promoción
@promocion_bp.route('/promociones', methods=['POST'])
@token_required_admin  # Protege este endpoint si es necesario
def agregar_promocion():
    data = request.get_json()
    descripcion = data.get('descripcion')
    fecha_inicio = data.get('fecha_inicio')
    fecha_fin = data.get('fecha_fin')

    if not (descripcion and fecha_inicio and fecha_fin):
        return jsonify({"error": "La descripción, fecha de inicio y fecha de fin son requeridos"}), 400

    try:
        fecha_inicio = datetime.fromisoformat(fecha_inicio)
        fecha_fin = datetime.fromisoformat(fecha_fin)
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido"}), 400

    if fecha_fin <= fecha_inicio:
        return jsonify({"error": "La fecha de fin debe ser después de la fecha de inicio"}), 400

    nueva_promocion = Promocion(
        descripcion=descripcion,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )

    try:
        db.session.add(nueva_promocion)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al agregar la promoción: {str(e)}"}), 500

    return jsonify({"message": "Promoción agregada exitosamente"}), 201

'''Eliminar promocion'''
@promocion_bp.route('/promociones/<int:id>', methods=['DELETE'])
@token_required_admin  # Protege este endpoint si es necesario
def eliminar_promocion(id):
    promocion = Promocion.query.get(id)

    if not promocion:
        return jsonify({'error': 'La promoción no se encuentra en el catálogo'}), 404

    try:
        db.session.delete(promocion)
        db.session.commit()
        return jsonify({"message": "Promoción eliminada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al eliminar la promoción: {str(e)}"}), 500

'''editar promocion'''
@promocion_bp.route('/promociones/<int:id>', methods=['PUT'])
@token_required_admin  # Protege este endpoint si es necesario
def editar_promocion(id):
    promocion = Promocion.query.get(id)

    if not promocion:
        return jsonify({'error': 'La promoción no se encuentra en el catálogo'}), 404

    data = request.get_json()

    descripcion = data.get('descripcion', promocion.descripcion)
    fecha_inicio = data.get('fecha_inicio', promocion.fecha_inicio.isoformat() if promocion.fecha_inicio else None)
    fecha_fin = data.get('fecha_fin', promocion.fecha_fin.isoformat() if promocion.fecha_fin else None)

    try:
        if fecha_inicio:
            fecha_inicio = datetime.fromisoformat(fecha_inicio)
        if fecha_fin:
            fecha_fin = datetime.fromisoformat(fecha_fin)
    except ValueError:
        return jsonify({"error": "Formato de fecha inválido"}), 400

    # Actualizar los campos
    promocion.descripcion = descripcion
    promocion.fecha_inicio = fecha_inicio
    promocion.fecha_fin = fecha_fin

    try:
        db.session.commit()
        return jsonify({"message": "Promoción modificada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al modificar la promoción: {str(e)}"}), 500