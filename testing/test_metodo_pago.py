import pytest
from app.models.metodo_pago import MetodoPago


def test_obtener_metodo_pago_por_id(client, token, metodos_pago):
    """Test para obtener un método de pago por su ID utilizando el fixture de metodos_pago"""
    
    # Usa el primer método de pago creado en el fixture
    metodo_pago_1 = metodos_pago[0]
    
    # Headers con el token para autenticación
    headers = {'Authorization': f'{token}'}
    
    # Realiza la solicitud GET para obtener el método de pago por ID
    response = client.get(f'/api/metodos_pago/{metodo_pago_1.id}', headers=headers)
    
    # Verifica que la respuesta sea 200 (éxito)
    assert response.status_code == 200
    
def test_editar_metodo_pago(client, token, metodos_pago):
    """Test para editar el tipo de un método de pago usando el ID del método creado"""
    
    # Usa el primer método de pago creado en el fixture
    metodo_pago_1 = metodos_pago[0]
    
    # Nuevos datos para editar
    data = {'tipo': 'Transferencia Bancaria'}
    
    # Headers con el token para autenticación
    headers = {'Authorization': f'{token}'}
    
    # Realiza la solicitud PUT para editar el método de pago
    response = client.put(f'/api/metodos_pago/{metodo_pago_1.id}', json=data, headers=headers)
    
    # Verifica que la respuesta sea 200 (éxito)
    assert response.status_code == 200

    
def test_obtener_metodos_pago(client, token, metodos_pago):
    """Test para obtener todos los métodos de pago"""

    # Headers con el token para autenticación
    headers = {'Authorization': f'{token}'}

    # Realiza la solicitud GET para obtener todos los métodos de pago
    response = client.get('/api/metodos_pago', headers=headers)

    # Verifica que la respuesta sea 200 (éxito)
    assert response.status_code == 200

def test_eliminar_metodo_pago(client, token, metodos_pago):
    """Test para eliminar un método de pago por ID"""

    # Usa el primer método de pago creado en el fixture
    metodo_pago_1 = metodos_pago[0]
    
    # Headers con el token para autenticación
    headers = {'Authorization': f'{token}'}
    
    # Realiza la solicitud DELETE para eliminar el método de pago
    response = client.delete(f'/api/metodos_pago/{metodo_pago_1.id}', headers=headers)
    
    # Verifica que la respuesta sea 200 (éxito)
    assert response.status_code == 200
    
    
