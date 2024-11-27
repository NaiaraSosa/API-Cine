import pytest
from app.models.reseña import Reseña
from app.models.pelicula import Pelicula
from app.models.usuario import Usuario
from app.connection import db

''' Prueba para obtener reseña por ID '''
def test_obtener_reseña(client, token, reseñas):
    reseña = reseñas[0]  

    headers = {'Authorization': f'{token}'}

    response = client.get(f'/api/reseñas/{reseña.id}', headers=headers)

    assert response.status_code == 200

''' Prueba para obtener reseñas '''
def test_obtener_reseñas(client, token, reseñas, peliculas):
    pelicula = peliculas[0]       
    headers = {'Authorization': f'{token}'}

    response = client.get(f'/api/reseñas/pelicula/{pelicula.id}', headers=headers)

    assert response.status_code == 200

    
''' Prueba para editar reseña por ID '''   
def test_editar_reseña(client, token, reseñas):
    reseña = reseñas[0]  
    new_data = {'calificacion': 4, 'comentario': "Muy buena película, la recomendaría."}

    headers = {'Authorization': f'{token}'}

    response = client.put(f'/api/reseñas/{reseña.id}', json=new_data, headers=headers)

    assert response.status_code == 200

''' Prueba para eliminar reseña por ID '''
def test_eliminar_reseña(client, token, reseñas):
    reseña = reseñas[0]  
    
    headers = {'Authorization': f'{token}'}


    response = client.delete(f'/api/reseñas/{reseña.id}', headers=headers)

    assert response.status_code == 200
