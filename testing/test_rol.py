import pytest
from app.models.rol import Rol

''' Prueba para obtener rol por ID '''
def test_obtener_rol(client, token, rol):
    rol_id = rol.id
    
    headers = {'Authorization': f'{token}'}

    response = client.get(f'/api/roles/{rol_id}', headers=headers)

    assert response.status_code == 200

''' Prueba para obtener roles '''
def test_obtener_roles(client, token):
    headers = {'Authorization': f'{token}'}

    response = client.get('/api/roles', headers=headers)

    assert response.status_code == 200


''' Prueba para editar rol por ID '''
def test_editar_rol(client, token, rol):
    rol_id = rol.id
    data = {'nombre': 'Moderador'}

    headers = {'Authorization': f'{token}'}

    response = client.put(f'/api/roles/{rol_id}', json=data, headers=headers)

    assert response.status_code == 200


''' Prueba para eliminar rol por ID '''
def test_eliminar_rol(client, token, rol):   
    rol_id = rol.id

    headers = {'Authorization': f'{token}'}

    response = client.delete(f'/api/roles/{rol_id}', headers=headers)

    assert response.status_code == 200

