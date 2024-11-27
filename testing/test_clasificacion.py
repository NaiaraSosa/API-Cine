import pytest
from app.models.clasificacion import Clasificacion

''' Prueba para obtener clasificiacion por ID '''
def test_obtener_clasificacion(client, token, clasificacion):
    clasificacion_id = clasificacion.id

    headers = {'Authorization': f'{token}'}

    response = client.get(f'/api/clasificaciones/{clasificacion_id}', headers=headers)

    assert response.status_code == 200

''' Prueba para obtener clasificiaciones '''
def test_obtener_clasificaciones(client, token):
    headers = {'Authorization': f'{token}'}

    response = client.get('/api/clasificaciones', headers=headers)

    assert response.status_code == 200

''' Prueba para editar clasificacion por ID '''
def test_editar_clasificacion(client, token, clasificacion):
    clasificacion_id = clasificacion.id
    
    data = {'codigo': 'pg25'}
    
    headers = {'Authorization': f'{token}'}

    response = client.put(f'/api/clasificaciones/{clasificacion_id}', json=data, headers=headers)

    assert response.status_code == 200

''' Prueba para eliminar clasificiacion por ID '''
def test_eliminar_clasificacion(client, token, clasificacion):
    clasificacion_id = clasificacion.id

    headers = {'Authorization': f'{token}'}

    response = client.delete(f'/api/clasificaciones/{clasificacion_id}', headers=headers)

    assert response.status_code == 200

