from flask import Blueprint, request, jsonify
from app.connection import db
from app.models.metodo_pago import MetodoPago
from app.routes.usuario_routes import token_required, token_required_admin

metodo_pago_bp = Blueprint('metodo_pago_bp', __name__)

''' Obtener metodo de pago por ID '''
@metodo_pago_bp.route('/metodos_pago/<int:id>', methods=['GET'])
@token_required_admin
def obtener_metodo_pago(id):
    metodo_pago = MetodoPago.query.get(id)
    if not metodo_pago:
        return jsonify({'error': 'El metodo de pago no se encuentra en el catalogo'}), 404

    metodo_pago_data = {
        'id': metodo_pago.id,
        'tipo': metodo_pago.tipo
    }

    return jsonify(metodo_pago_data), 200


''' Obtener todos los metodos de pago por ID '''
@metodo_pago_bp.route('/metodos_pago', methods=['GET'])
@token_required_admin
def obtener_metodos_pago():
    metodos_pago = MetodoPago.query.all()
    metodos_pago_data = [{'id': metodo.id, 'tipo': metodo.tipo} for metodo in metodos_pago]

    return jsonify(metodos_pago_data), 200

''' Agregar metodo de pago '''
@metodo_pago_bp.route('/metodos_pago', methods=['POST'])
@token_required_admin
def agregar_metodo_pago():
    data = request.get_json()
    tipo = data.get('tipo')

    if not tipo:
        return jsonify({"error": "El tipo del metodo de pago es requerido"}), 400

    nuevo_metodo_pago = MetodoPago(tipo=tipo)

    try:
        db.session.add(nuevo_metodo_pago)
        db.session.commit()
        return jsonify({"message": "Metodo de pago agregado exitosamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al agregar el metodo de pago: {str(e)}"}), 500


''' Eliminar metodo de pago por ID '''
@metodo_pago_bp.route('/metodos_pago/<int:id>', methods=['DELETE'])
@token_required_admin
def eliminar_metodo_pago(id):
    metodo_pago = MetodoPago.query.get(id)

    if not metodo_pago:
        return jsonify({'error': 'El metodo de pago no se encuentra en el catalogo'}), 404

    try:
        db.session.delete(metodo_pago)
        db.session.commit()
        return jsonify({"message": "Metodo de pago eliminado exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al eliminar el metodo de pago: {str(e)}"}), 500


''' Editar metodo de pago por ID '''
@metodo_pago_bp.route('/metodos_pago/<int:id>', methods=['PUT'])
@token_required_admin
def editar_metodo_pago(id):
    metodo_pago = MetodoPago.query.get(id)

    if not metodo_pago:
        return jsonify({'error': 'El metodo de pago no se encuentra en el catalogo'}), 404

    data = request.get_json()
    tipo = data.get('tipo', metodo_pago.tipo)

    metodo_pago.tipo = tipo

    try:
        db.session.commit()
        return jsonify({"message": "Metodo de pago modificado exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al modificar el metodo de pago: {str(e)}"}), 500
