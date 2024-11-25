from flask import Blueprint, request, jsonify
from app.connection import db
from app.models.producto import Producto
from app.routes.usuario_routes import token_required, token_required_admin

producto_bp = Blueprint('producto_bp', __name__)

# Obtener un Producto por ID
@producto_bp.route('/productos/<int:id>', methods=['GET'])
@token_required_admin
def obtener_producto(id):
    producto = Producto.query.get(id)
    if not producto:
        return jsonify({'error': 'El producto no se encuentra en el catálogo'}), 404

    producto_data = {
        'id': producto.id,
        'nombre': producto.nombre,
        'precio': str(producto.precio)  # Convertir a string para evitar problemas de serialización
    }

    return jsonify(producto_data), 200


# Obtener todos los Productos
@producto_bp.route('/productos', methods=['GET'])
@token_required_admin
def obtener_productos():
    productos = Producto.query.all()
    productos_data = [{'id': producto.id, 'nombre': producto.nombre, 'precio': str(producto.precio)} for producto in productos]

    return jsonify(productos_data), 200


# Agregar un nuevo Producto
@producto_bp.route('/productos', methods=['POST'])
@token_required_admin
def agregar_producto():
    data = request.get_json()
    nombre = data.get('nombre')
    precio = data.get('precio')

    if not nombre or precio is None:
        return jsonify({"error": "El nombre y el precio del producto son requeridos"}), 400

    try:
        precio = float(precio)
        if precio < 0:
            return jsonify({"error": "El precio no puede ser negativo"}), 400
    except ValueError:
        return jsonify({"error": "El precio debe ser un número válido"}), 400

    nuevo_producto = Producto(nombre=nombre, precio=precio)

    try:
        db.session.add(nuevo_producto)
        db.session.commit()
        return jsonify({"message": "Producto agregado exitosamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al agregar el producto: {str(e)}"}), 500


# Eliminar un Producto por ID
@producto_bp.route('/productos/<int:id>', methods=['DELETE'])
@token_required_admin
def eliminar_producto(id):
    producto = Producto.query.get(id)

    if not producto:
        return jsonify({'error': 'El producto no se encuentra en el catálogo'}), 404

    try:
        db.session.delete(producto)
        db.session.commit()
        return jsonify({"message": "Producto eliminado exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al eliminar el producto: {str(e)}"}), 500


# Editar un Producto por ID
@producto_bp.route('/productos/<int:id>', methods=['PUT'])
@token_required_admin
def editar_producto(id):
    producto = Producto.query.get(id)

    if not producto:
        return jsonify({'error': 'El producto no se encuentra en el catálogo'}), 404

    data = request.get_json()
    nombre = data.get('nombre', producto.nombre)
    precio = data.get('precio', producto.precio)

    try:
        if precio is not None:
            precio = float(precio)
            if precio < 0:
                return jsonify({"error": "El precio no puede ser negativo"}), 400
    except ValueError:
        return jsonify({"error": "El precio debe ser un número válido"}), 400

    producto.nombre = nombre
    producto.precio = precio

    try:
        db.session.commit()
        return jsonify({"message": "Producto modificado exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al modificar el producto: {str(e)}"}), 500
