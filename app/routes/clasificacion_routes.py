from flask import Blueprint, request, jsonify
from app.connection import db
from app.models.clasificacion import Clasificacion
from app.routes.usuario_routes import token_required, token_required_admin

clasificacion_bp = Blueprint('clasificacion_bp', __name__)

''' Obtener clasificacion por ID '''
@clasificacion_bp.route('/clasificaciones/<int:id>', methods=['GET'])
@token_required_admin
def obtener_clasificacion(id):
    clasificacion = Clasificacion.query.get(id)
    if not clasificacion:
        return jsonify({'error': 'La clasificacion no se encuentra en el catalogo'}), 404

    clasificacion_data = {
        'id': clasificacion.id,
        'codigo': clasificacion.codigo
    }

    return jsonify(clasificacion_data), 200


''' Obtener todas las clasificaciones '''
@clasificacion_bp.route('/clasificaciones', methods=['GET'])
@token_required_admin
def obtener_clasificaciones():
    clasificaciones = Clasificacion.query.all()
    clasificaciones_data = [{'id': clasificacion.id, 'codigo': clasificacion.codigo} for clasificacion in clasificaciones]

    return jsonify(clasificaciones_data), 200


''' Agregar una clasificacion '''
@clasificacion_bp.route('/clasificaciones', methods=['POST'])
@token_required_admin
def agregar_clasificacion():
    data = request.get_json()
    codigo = data.get('codigo')

    if not codigo:
        return jsonify({"error": "El codigo de la clasificacion es requerido"}), 400

    nueva_clasificacion = Clasificacion(codigo=codigo)

    try:
        db.session.add(nueva_clasificacion)
        db.session.commit()
        return jsonify({"message": "Clasificacion agregada exitosamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al agregar la clasificacion: {str(e)}"}), 500


''' Eliminar una clasificacion por ID '''
@clasificacion_bp.route('/clasificaciones/<int:id>', methods=['DELETE'])
@token_required_admin
def eliminar_clasificacion(id):
    clasificacion = Clasificacion.query.get(id)

    if not clasificacion:
        return jsonify({'error': 'La clasificacion no se encuentra en el catalogo'}), 404

    try:
        db.session.delete(clasificacion)
        db.session.commit()
        return jsonify({"message": "clasificacion eliminada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al eliminar la clasificacion: {str(e)}"}), 500


''' Editar una clasificacion por ID '''
@clasificacion_bp.route('/clasificaciones/<int:id>', methods=['PUT'])
@token_required_admin
def editar_clasificacion(id):
    clasificacion = Clasificacion.query.get(id)

    if not clasificacion:
        return jsonify({'error': 'La clasificacion no se encuentra en el catalogo'}), 404

    data = request.get_json()
    codigo = data.get('codigo', clasificacion.codigo)

    clasificacion.codigo = codigo

    try:
        db.session.commit()
        return jsonify({"message": "clasificacion modificada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al modificar la clasificacion: {str(e)}"}), 500
