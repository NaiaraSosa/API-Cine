import pytest
from app.models.metodo_pago import MetodoPago

''' Prueba para obtener metodo de pago por ID '''
def test_obtener_metodo(client, token, metodos_pago):
    metodo_pago_1 = metodos_pago[0]
    
    headers = {'Authorization': f'{token}'}
    
    response = client.get(f'/api/metodos_pago/{metodo_pago_1.id}', headers=headers)
    
    assert response.status_code == 200
    
''' Prueba para editar metodo de pago por ID '''
def test_editar_metodo_pago(client, token, metodos_pago):
    metodo_pago_1 = metodos_pago[0]

    data = {'tipo': 'Transferencia Bancaria'}

    headers = {'Authorization': f'{token}'}

    response = client.put(f'/api/metodos_pago/{metodo_pago_1.id}', json=data, headers=headers)

    assert response.status_code == 200

''' Prueba para obtener metodos de pago '''
def test_obtener_metodos_pago(client, token, metodos_pago):
    headers = {'Authorization': f'{token}'}

    response = client.get('/api/metodos_pago', headers=headers)

    assert response.status_code == 200

''' Prueba para eliminar metodo de pago por ID '''
def test_eliminar_metodo_pago(client, token, metodos_pago):
    metodo_pago_1 = metodos_pago[0]
    
    headers = {'Authorization': f'{token}'}
    
    response = client.delete(f'/api/metodos_pago/{metodo_pago_1.id}', headers=headers)
    
    assert response.status_code == 200

