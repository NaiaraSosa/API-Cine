import pytest
from app.models.producto import Producto


def test_comprar_productos(client, token, productos, metodos_pago):
    metodo_pago = metodos_pago[0] 
    producto = productos[0]

    headers = {"Authorization": f'{token}'}  # Asegúrate de incluir el token correctamente
    
    # Datos de compra con un producto y un método de pago
    compra_data = {
        "productos": [
            {"id_producto": producto.id, "cantidad": 2},  # Compramos 2 unidades del producto
        ],
        "id_metodo_pago": metodo_pago.id  # Usamos el primer método de pago
    }
    
    # Realizamos la compra
    response = client.post("/api/productos/comprar", json=compra_data, headers=headers)
    
    # Verificamos el estado de la respuesta
    assert response.status_code == 201  # Se espera un código 201 si la compra fue exitosa


def test_obtener_producto(client, token, productos):
    producto = productos[0]
    headers = {"Authorization": f'{token}'}
    response = client.get(f"/api/productos/{producto.id}", headers=headers)
    assert response.status_code == 200

def test_eliminar_producto(client, token, productos):
    producto = productos[1]
    headers = {"Authorization": f'{token}'}
    response = client.delete(f"/api/productos/{producto.id}", headers=headers)
    assert response.status_code == 200

def test_editar_producto(client, token, productos):
    producto = productos[0]
    headers = {"Authorization": f'{token}'}
    updated_data = {"nombre": "Producto A Editado", "precio": 150.0}

    response = client.put(f"/api/productos/{producto.id}", json=updated_data, headers=headers)
    assert response.status_code == 200

def test_obtener_productos(client, token, productos):
    headers = {"Authorization": f'{token}'}
    response = client.get("/api/productos", headers=headers)
    assert response.status_code == 200

