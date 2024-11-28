import pytest
from app.models.pelicula import Pelicula
from app.models.clasificacion import Clasificacion

''' Prueba para obtener pelicula por ID '''
def test_obtener_pelicula(client, token, peliculas):
    pelicula = peliculas[0]  
    
    headers = {'Authorization': f'{token}'}
    response = client.get(f'/api/peliculas/{pelicula.id}', headers=headers)

    assert response.status_code == 200

''' Prueba para editar pelicula por ID '''  
def test_editar_pelicula(client, token, peliculas):
    pelicula = peliculas[0] 
    
    data = {
        'titulo': 'Pelicula Editada', 
        'director': 'Director Editado', 
        'duracion': 140, 
        'id_clasificacion': pelicula.id_clasificacion, 
        'sinopsis': 'Sinopsis actualizada de la película'
    }

    headers = {'Authorization': f'{token}'}
    
    response = client.put(f'/api/peliculas/{pelicula.id}', json=data, headers=headers)

    assert response.status_code == 200

''' Prueba para eliminar pelicula por ID ''' 
def test_eliminar_pelicula(client, token, peliculas):
    pelicula = peliculas[0]  
    
    headers = {'Authorization': f'{token}'}
    
    response = client.delete(f'/api/peliculas/{pelicula.id}', headers=headers)

    assert response.status_code == 200

''' Prueba para obtener peliculas '''
def test_obtener_peliculas(client, token, peliculas):
    headers = {'Authorization': f'{token}'}
    
    response = client.get('/api/peliculas', headers=headers)

    assert response.status_code == 200
