"""
Archivo: configuracion_routes.py
Descripción: Este archivo contiene las rutas relacionadas con la configuración general de la aplicación.
Incluye operaciones para agregar, actualizar y obtener la configuración, como el precio de la entrada.
"""
from flask import Blueprint, request, jsonify
from app.connection import db
from app.models.configuracion import Configuracion
from app.routes.usuario_routes import token_required_admin

config_bp = Blueprint('config_bp', __name__)

'''Agregar o actualizar configuración general'''
@config_bp.route('/configuracion', methods=['POST'])
@token_required_admin
def agregar_actualizar_configuracion():
    """
    Agregar o actualizar una configuración general.

    Cuerpo de la solicitud:
    - clave (str): Clave de la configuración.
    - valor (str): Valor de la configuración.

    Retorna:
    - 201: Mensaje de éxito con los detalles de la configuración.
    - 400: Error si no se proporciona la clave o el valor.
    - 500: Error al guardar la configuración en la base de datos.
    """
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
    


@config_bp.route('/precio-entrada', methods=['GET'])
@token_required_admin
def obtener_precio_entrada():
    """
    Obtener el precio de la entrada configurado en la aplicación.

    Retorna:
    - 200: El precio de la entrada en formato JSON.
    - 404: Mensaje de error si no se encuentra el precio configurado.
    """
    precio_config = Configuracion.query.filter_by(clave='precio_entrada').first()
    if not precio_config:
        return jsonify({'error': 'Precio de entrada no configurado'}), 404
    
    return jsonify({'precio_entrada': float(precio_config.valor)}), 200



@config_bp.route('/precio-entrada', methods=['PUT'])
@token_required_admin
def actualizar_precio_entrada():
    """
    Actualizar el precio de la entrada en la configuración de la aplicación.

    Cuerpo de la solicitud:
    - precio_entrada (float): Nuevo precio para la entrada.

    Retorna:
    - 200: Mensaje de éxito si se actualiza el precio de entrada.
    - 400: Error si el precio no es un número válido o es negativo.
    - 500: Error al actualizar el precio en la base de datos.
    """
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

