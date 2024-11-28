"""
Archivo: producto_routes.py
Descripción: Este archivo contiene las rutas relacionadas con los productos en la aplicación.
Incluye operaciones para obtener, crear, editar y eliminar productos, además de poder comprarlos.
"""
from flask import Blueprint, request, jsonify
from app.connection import db
from app.models.detalle_trans_producto import DetalleTransaccionProducto
from app.models.producto import Producto
from app.models.transaccion_producto import TransaccionProductos
from app.routes.usuario_routes import token_required, token_required_admin

producto_bp = Blueprint('producto_bp', __name__)

@producto_bp.route('/productos/<int:id>', methods=['GET'])
@token_required
def obtener_producto(id, id_usuario):
    """
    Obtener un producto por su ID.

    Parámetros:
    id (int): El ID del producto a obtener.

    Retorna:
    - 200: Detalles del producto en formato JSON.
    - 404: Mensaje de error si no se encuentra el producto.
    """
    producto = Producto.query.get(id)
    if not producto:
        return jsonify({'error': 'El producto no se encuentra en el catálogo'}), 404

    producto_data = {
        'id': producto.id,
        'nombre': producto.nombre,
        'precio': producto.precio
    }

    return jsonify(producto_data), 200


@producto_bp.route('/productos', methods=['GET'])
@token_required
def obtener_productos(id_usuario):
    """
    Obtener todos los productos.

    Retorna:
    - 200: Lista de productos en formato JSON.
    - 404: Mensaje de error si no se encuentran productos.
    """
    productos = Producto.query.all()
    if not productos:
        return jsonify({"message": "No se encontraron productos en el catálogo"}), 404
    
    productos_data = [{'id': producto.id, 'nombre': producto.nombre, 'precio': producto.precio} for producto in productos]

    return jsonify(productos_data), 200


'''Agregar un nuevo producto'''
@producto_bp.route('/productos', methods=['POST'])
@token_required_admin
def agregar_producto():
    """
    Agregar un nuevo producto.

    Cuerpo de la solicitud:
    - nombre (str): Nombre del producto.
    - precio (float): Precio del producto.

    Retorna:
    - 201: Mensaje de éxito con los detalles del producto creado.
    - 400: Error si los datos de entrada son inválidos.
    - 409: Error si el producto ya existe en el catálogo.
    - 500: Error si ocurre un problema al agregar el producto.
    """
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

    # Validación de duplicados
    producto_existente = Producto.query.filter_by(nombre=nombre).first()
    if producto_existente:
        return jsonify({"error": f"Ya existe un producto con el nombre '{nombre}'"}), 409
    
    nuevo_producto = Producto(nombre=nombre, precio=precio)

    try:
        db.session.add(nuevo_producto)
        db.session.commit()
        return jsonify({"message": "Producto agregado exitosamente", 
                        "producto": {"id": nuevo_producto.id, "nombre": nombre, "precio": precio}}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al agregar el producto: {str(e)}"}), 500



'''Editar un producto'''
@producto_bp.route('/productos/<int:id>', methods=['PUT'])
@token_required_admin
def editar_producto(id):
    """
    Editar un producto existente.

    Parámetros:
    id (int): El ID del producto a editar.

    Cuerpo de la solicitud:
    - nombre (str): Nombre del producto.
    - precio (float): Precio del producto.

    Retorna:
    - 200: Mensaje de éxito con los detalles del producto editado.
    - 400: Error si el precio no es válido o el nombre es duplicado.
    - 404: Error si no se encuentra el producto.
    - 500: Error si ocurre un problema al editar el producto.
    """
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

    # Validación de nombre duplicado (excluyendo el producto actual)
    if nombre != producto.nombre:
        producto_existente = Producto.query.filter_by(nombre=nombre).first()
        if producto_existente:
            return jsonify({"error": f"Ya existe un producto con el nombre '{nombre}'"}), 409
        
    producto.nombre = nombre
    producto.precio = precio

    try:
        db.session.commit()
        return jsonify({"message": "Producto modificado exitosamente",
                        "producto": {"id": producto.id, "nombre": nombre, "precio": precio}}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al modificar el producto: {str(e)}"}), 500



'''Eliminar un producto'''
@producto_bp.route('/productos/<int:id>', methods=['DELETE'])
@token_required_admin
def eliminar_producto(id):
    """
    Eliminar un producto del catálogo.

    Parámetros:
    id (int): El ID del producto a eliminar.

    Retorna:
    - 200: Mensaje de éxito indicando que el producto ha sido eliminado.
    - 404: Error si no se encuentra el producto.
    - 500: Error si ocurre un problema al eliminar el producto.
    """
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
    

@producto_bp.route('/productos/comprar', methods=['POST'])
@token_required
def comprar_productos(id_usuario):
    """
    Realizar la compra de productos.

    Parámetros:
    - productos (list): Lista de productos con sus cantidades.
    - id_metodo_pago (int): El ID del método de pago seleccionado.

    Retorna:
    - 201: Mensaje de éxito con los detalles de la transacción.
    - 400: Error si los datos de entrada son inválidos.
    - 500: Error si ocurre un problema al procesar la compra.
    """
    data = request.get_json()
    productos = data.get('productos')
    id_metodo_pago = data.get('id_metodo_pago')

    # Validaciones y lógica principal siguen igual
    if not productos or not id_metodo_pago:
        return jsonify({"error": "Los productos y el método de pago son requeridos"}), 400

    total = 0
    detalles = []

    # Validar cada prod y calcular subtotal
    for item in productos:
        id_producto = item.get('id_producto')
        cantidad = item.get('cantidad')

        if not id_producto or not cantidad or cantidad <= 0:
            return jsonify({"error": f"Datos inválidos para el producto {id_producto}"}), 400
        
        producto = Producto.query.get(id_producto)
        if not producto:
            return jsonify({"error": f"El producto con ID {id_producto} no existe"}), 404
        
        subtotal = float(producto.precio) * cantidad
        total += subtotal

        # Crear un detalle de la transacción
        detalle = DetalleTransaccionProducto(
            id_producto=id_producto,
            cantidad=cantidad,
            subtotal=subtotal
        )
        detalles.append(detalle)   

    # Crear la transacción principal
    transaccion = TransaccionProductos(
        id_usuario=id_usuario,
        total=total,
        id_metodo_pago=id_metodo_pago
    )

    db.session.add(transaccion)

    try:
        db.session.flush()  
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al crear la transacción: {str(e)}"}), 500

    # Asociar detalles a la transacción
    for detalle in detalles:
        detalle.id_transaccion = transaccion.id
        db.session.add(detalle)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al procesar la compra: {str(e)}"}), 500

    return jsonify({
        "message": "Compra realizada con éxito",
        "transaccion": {
            "id": transaccion.id,
            "id_usuario": transaccion.id_usuario,
            "total": float(transaccion.total),
            "id_metodo_pago": transaccion.id_metodo_pago,
            "fecha_compra": transaccion.fecha_compra,
            "detalles": [
                {
                    "id_producto": detalle.id_producto,
                    "cantidad": detalle.cantidad,
                    "subtotal": float(detalle.subtotal)
                } for detalle in detalles
            ]
        }
    }), 201

