from flask import Blueprint, request, jsonify
from app.connection import db
from app.models.configuracion import Configuracion
from app.routes.usuario_routes import token_required_admin

config_bp = Blueprint('config_bp', __name__)

'''Agregar o actualizar configuración general'''
@config_bp.route('/configuracion', methods=['POST'])
@token_required_admin
def agregar_actualizar_configuracion():
    data = request.get_json()
    clave = data.get('clave')
    valor = data.get('valor')

    if not clave or not valor:
        return jsonify({'error': 'La clave y el valor son requeridos'}), 400

    configuracion = Configuracion.query.filter_by(clave=clave).first()

    if configuracion:
        configuracion.valor = valor
        mensaje = 'Configuración actualizada exitosamente'
    else:
        configuracion = Configuracion(clave=clave, valor=valor)
        db.session.add(configuracion)
        mensaje = 'Configuración agregada exitosamente'

    try:
        db.session.commit()
        return jsonify({'message': mensaje, 'clave': clave, 'valor': valor}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al guardar la configuración: {str(e)}'}), 500
    


'''Obtener el precio de la entrada'''
@config_bp.route('/precio-entrada', methods=['GET'])
@token_required_admin
def obtener_precio_entrada():
    precio_config = Configuracion.query.filter_by(clave='precio_entrada').first()
    if not precio_config:
        return jsonify({'error': 'Precio de entrada no configurado'}), 404
    
    return jsonify({'precio_entrada': float(precio_config.valor)}), 200



'''Actualizar el precio de la entrada'''
@config_bp.route('/precio-entrada', methods=['PUT'])
@token_required_admin
def actualizar_precio_entrada():
    data = request.get_json()
    nuevo_precio = data.get('precio_entrada')

    # Validar que el precio sea un número flotante positivo
    try:
        nuevo_precio = float(nuevo_precio)
        if nuevo_precio < 0:
            return jsonify({'error': 'El precio no puede ser negativo'}), 400
    except ValueError:
        return jsonify({'error': 'El precio debe ser un número válido'}), 400

    # Verificar si ya existe una configuración para el precio
    precio_config = Configuracion.query.filter_by(clave='precio_entrada').first()

    if not precio_config:
        # Si no existe, podemos agregarlo directamente
        precio_config = Configuracion(clave='precio_entrada', valor=str(nuevo_precio))
        db.session.add(precio_config)
        mensaje = 'Precio de entrada agregado exitosamente'
    else:
        # Si existe, actualizamos el valor
        precio_config.valor = str(nuevo_precio)
        mensaje = 'Precio de entrada actualizado exitosamente'

    try:
        db.session.commit()
        return jsonify({'message': mensaje}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error al actualizar el precio: {str(e)}'}), 500

