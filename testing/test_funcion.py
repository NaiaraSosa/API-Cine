import pytest
from app.models.funcion import Funcion
from app.models.pelicula import Pelicula
from app.models.sala import Sala
from datetime import datetime, timedelta

''' Prueba para obtener funcion por ID'''
def test_obtener_funcion_id(client, token, funciones):
    funcion = funciones [0]
    headers = {"Authorization": f'{token}'}
    
    response = client.get(f"/api/funciones/{funcion.id}", headers=headers)
    assert response.status_code == 200



''' Prueba para obtener funciones por pelicula'''
def test_obtener_funciones_pelicula(client, token, funciones, peliculas):
    pelicula = peliculas[0]
    headers = {"Authorization": f'{token}'}
    
    response = client.get(f"/api/funciones/pelicula/{pelicula.id}", headers=headers)
    assert response.status_code == 200

''' Prueba para agregar una función '''
def test_agregar_funcion(client, token, peliculas, salas):
    pelicula = peliculas[0]
    sala = salas[0]
    headers = {"Authorization": f'{token}'}
    
    data = {
        "id_pelicula": pelicula.id,
        "id_sala": sala.id,
        "horario_inicio": "2024-12-03T18:00:00",
        "horario_fin": "2024-12-03T20:00:00"
    }
    
    response = client.post("/api/funciones", json=data, headers=headers)
    assert response.status_code == 201


''' Prueba para editar una función '''
def test_editar_funcion(client, token, funciones):
    funcion = funciones[0]
    headers = {"Authorization": f'{token}'}    
    data = {
        "id_pelicula": funcion.id_pelicula,
        "id_sala": funcion.id_sala,
        "horario_inicio": "2024-12-01T19:00:00",
        "horario_fin": "2024-12-01T21:00:00"
    }
    
    response = client.put(f"/api/funciones/{funcion.id}", json=data, headers=headers)
    assert response.status_code == 200


''' Prueba para eliminar una función '''
def test_eliminar_funcion(client, token, funciones):
    funcion = funciones[0]
    headers = {"Authorization": f'{token}'}
    
    response = client.delete(f"/api/funciones/{funcion.id}", headers=headers)
    assert response.status_code == 200

