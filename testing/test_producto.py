import pytest
from app.models.producto import Producto

''' Prueba para comprar productos '''
def test_comprar_productos(client, token, productos, metodos_pago):
    metodo_pago = metodos_pago[0] 
    producto = productos[0]

    headers = {"Authorization": f'{token}'}  
    
    compra_data = {
        "productos": [
            {"id_producto": producto.id, "cantidad": 2},  
        ],
        "id_metodo_pago": metodo_pago.id 
    }
    

    response = client.post("/api/productos/comprar", json=compra_data, headers=headers)
    

    assert response.status_code == 201 

''' Prueba para obtener productos '''
def test_obtener_producto(client, token, productos):
    producto = productos[0]
    headers = {"Authorization": f'{token}'}
    response = client.get(f"/api/productos/{producto.id}", headers=headers)
    assert response.status_code == 200


''' Prueba para eliminar producto por ID '''
def test_eliminar_producto(client, token, productos):
    producto = productos[1]
    headers = {"Authorization": f'{token}'}
    response = client.delete(f"/api/productos/{producto.id}", headers=headers)
    assert response.status_code == 200

''' Prueba para editar producto por ID'''
def test_editar_producto(client, token, productos):
    producto = productos[0]
    headers = {"Authorization": f'{token}'}
    updated_data = {"nombre": "Producto A Editado", "precio": 150.0}

    response = client.put(f"/api/productos/{producto.id}", json=updated_data, headers=headers)
    assert response.status_code == 200

''' Prueba para obtener productos '''
def test_obtener_productos(client, token, productos):
    headers = {"Authorization": f'{token}'}
    response = client.get("/api/productos", headers=headers)
    assert response.status_code == 200

