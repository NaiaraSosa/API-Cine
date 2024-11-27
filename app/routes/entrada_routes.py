from flask import request, jsonify, session, Blueprint
from app.connection import db
from app.models.entrada import Entrada
from app.models.transaccion_entrada import TransaccionEntrada
from app.models.funcion import Funcion
from app.models.metodo_pago import MetodoPago
from app.models.configuracion import Configuracion
from app.routes.usuario_routes import token_required


entrada_bp = Blueprint('entrada_bp', __name__)


'''Comprar entradas'''
@entrada_bp.route('/entradas', methods=['POST'])
@token_required
def comprar_entradas(id_usuario):
    data = request.get_json()
    id_funcion = data.get('id_funcion')
    cantidad = data.get('cantidad')
    id_metodo_pago = data.get('id_metodo_pago')

    # Validaciones y lógica principal siguen igual
    if not (id_funcion and cantidad and id_metodo_pago):
        return jsonify({"error": "Todos los campos son requeridos"}), 400

    # Validar función existente
    funcion = Funcion.query.get(id_funcion)
    if not funcion:
        return jsonify({"error": "La función no existe"}), 404

    # Validar método de pago
    metodo_pago = MetodoPago.query.get(id_metodo_pago)
    if not metodo_pago:
        return jsonify({"error": "El método de pago no es válido"}), 404
    

    # Validar asientos disponibles
    if funcion.asientos_disponibles < cantidad:
        return jsonify({"error": f"Solo quedan {funcion.asientos_disponibles} asientos disponibles para esta función"}), 409

    # Obtener el precio de la entrada desde la tabla de configuraciones
    precio_config = Configuracion.query.filter_by(clave='precio_entrada').first()
    if not precio_config:
        return jsonify({'error': 'El precio de la entrada no está configurado'}), 500

    precio_por_entrada = float(precio_config.valor)  
    total = cantidad * precio_por_entrada
    
    # Crear transacción
    transaccion = TransaccionEntrada(
        id_usuario=id_usuario,
        id_funcion=id_funcion,
        cantidad_entradas=cantidad,
        total=total,
        id_metodo_pago=id_metodo_pago
    )
    db.session.add(transaccion)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al procesar la compra: {str(e)}"}), 500

    entradas = []
    for _ in range(cantidad):
        entrada = Entrada(
            id_funcion=id_funcion,
            id_transaccion=transaccion.id  
        )
        entradas.append(entrada)
        db.session.add(entrada)

    # Actualizar asientos disponibles
    funcion.asientos_disponibles -= cantidad

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al procesar la compra: {str(e)}"}), 500

    return jsonify({
        "message": "Compra realizada con éxito",
        "transaccion": {
            "id": transaccion.id,
            "id_usuario": id_usuario,
            "id_funcion": id_funcion,
            "cantidad_entradas": cantidad,
            "total": total,
            "fecha": transaccion.fecha
        },
        "entradas": [{"id": entrada.id, "id_funcion": entrada.id_funcion} for entrada in entradas]
    }), 201



'''Historial de compra de entradas'''
@entrada_bp.route('/entradas', methods=['GET'])
@token_required
def obtener_historial_entradas(id_usuario):
    transacciones = TransaccionEntrada.query.filter_by(id_usuario=id_usuario).all()

    if not transacciones:
        return jsonify({"message": "No tienes historial de compras."}), 200
    
    historial = []
    for transaccion in transacciones:
        entradas = Entrada.query.filter_by(id_transaccion=transaccion.id).all()

        historial.append({
            "id_transaccion": transaccion.id,
            "cantidad_entradas": transaccion.cantidad_entradas,
            "total": float(transaccion.total),
            "fecha": transaccion.fecha,
            "funcion": transaccion.id_funcion,  
            "entradas": [{"id_entrada": entrada.id, "id_funcion": entrada.id_funcion} for entrada in entradas]
        })
    
    return jsonify({"Historial de compra": historial}), 200


