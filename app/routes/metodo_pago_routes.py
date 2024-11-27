from flask import Blueprint, request, jsonify
from app.connection import db
from app.models.metodo_pago import MetodoPago
from app.routes.usuario_routes import token_required_admin

metodo_pago_bp = Blueprint('metodo_pago_bp', __name__)


''' Obtener un método de pago por ID '''
@metodo_pago_bp.route('/metodos_pago/<int:id>', methods=['GET'])
@token_required_admin
def obtener_metodo_pago(id):
    metodo_pago = MetodoPago.query.get(id)
    if not metodo_pago:
        return jsonify({'error': 'El método de pago no se encuentra en el catálogo'}), 404

    metodo_pago_data = {
        'id': metodo_pago.id,
        'tipo': metodo_pago.tipo
    }

    return jsonify(metodo_pago_data), 200



''' Obtener todos los métodos de pago '''
@metodo_pago_bp.route('/metodos_pago', methods=['GET'])
@token_required_admin
def obtener_metodos_pago():
    metodos_pago = MetodoPago.query.all()
    if not metodos_pago:
        return jsonify({"message": "No se encontraron métodos de pago"}), 404
    
    metodos_pago_data = [{'id': metodo.id, 'tipo': metodo.tipo} for metodo in metodos_pago]
    return jsonify(metodos_pago_data), 200



''' Agregar un nuevo Método de Pago '''
@metodo_pago_bp.route('/metodos_pago', methods=['POST'])
@token_required_admin
def agregar_metodo_pago():
    data = request.get_json()
    tipo = data.get('tipo')

    if not tipo:
        return jsonify({"error": "El tipo de método de pago es requerido"}), 400
    
    if MetodoPago.query.filter_by(tipo=tipo).first():
        return jsonify({"error": "El método de pago ya existe"}), 400

    nuevo_metodo_pago = MetodoPago(tipo=tipo)

    try:
        db.session.add(nuevo_metodo_pago)
        db.session.commit()
        return jsonify({"message": "Método de pago agregado exitosamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al agregar el método de pago: {str(e)}"}), 500



''' Editar un Método de Pago por ID '''
@metodo_pago_bp.route('/metodos_pago/<int:id>', methods=['PUT'])
@token_required_admin
def editar_metodo_pago(id):
    metodo_pago = MetodoPago.query.get(id)

    if not metodo_pago:
        return jsonify({'error': 'El método de pago no se encuentra en el catálogo'}), 404

    data = request.get_json()
    tipo = data.get('tipo', metodo_pago.tipo)

    if not tipo:
        return jsonify({'error': 'El tipo de método de pago es requerido'}), 400

    if tipo != metodo_pago.tipo and MetodoPago.query.filter_by(tipo=tipo).first():
        return jsonify({"error": "El método de pago ya existe"}), 400

    metodo_pago.tipo = tipo

    try:
        db.session.commit()
        return jsonify({"message": "Método de pago modificado exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al modificar el método de pago: {str(e)}"}), 500
    

    
''' Eliminar un Método de Pago por ID '''
@metodo_pago_bp.route('/metodos_pago/<int:id>', methods=['DELETE'])
@token_required_admin
def eliminar_metodo_pago(id):
    metodo_pago = MetodoPago.query.get(id)

    if not metodo_pago:
        return jsonify({'error': 'El método de pago no se encuentra en el catálogo'}), 404

    try:
        db.session.delete(metodo_pago)
        db.session.commit()
        return jsonify({"message": "Método de pago eliminado exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al eliminar el método de pago: {str(e)}"}), 500



