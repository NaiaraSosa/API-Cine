import pytest
from app.models.sala import Sala
from app.connection import db

''' Prueba para obtener sala por ID '''
def test_obtener_sala(client, token, salas):
    sala = salas[0]  

    headers = {'Authorization': f'{token}'}
    
    response = client.get(f'/api/salas/{sala.id}', headers=headers)

    assert response.status_code == 200

''' Prueba para editar sala por ID '''
def test_editar_sala(client, token, salas):
    sala = salas[0]  
    new_data = {'nombre': 'Sala Modificada', 'capacidad': 120}

    headers = {'Authorization': f'{token}'}
    
    response = client.put(f'/api/salas/{sala.id}', json=new_data, headers=headers)

    assert response.status_code == 200

''' Test para eliminar sala por ID '''
def test_eliminar_sala(client, token, salas):
    sala = salas[0]  

    headers = {'Authorization': f'{token}'}

    response = client.delete(f'/api/salas/{sala.id}', headers=headers)

    assert response.status_code == 200

''' Test para obtener todas las salas '''
def test_obtener_salas(client, token, salas):
    headers = {'Authorization': f'{token}'}

    response = client.get('/api/salas', headers=headers)

    assert response.status_code == 200
