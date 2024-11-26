import pytest
from app.models.pelicula import Pelicula
from app.models.clasificacion import Clasificacion

def test_obtener_pelicula(client, token, peliculas):
    """Test para obtener una película por ID"""
    pelicula = peliculas[0]  # Usamos la primera película creada en el fixture
    
    headers = {'Authorization': f'{token}'}
    response = client.get(f'/api/peliculas/{pelicula.id}', headers=headers)

    assert response.status_code == 200

    
def test_editar_pelicula(client, token, peliculas):
    """Test para editar una película"""
    pelicula = peliculas[0]  # Usamos la primera película creada en el fixture
    
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

    
def test_eliminar_pelicula(client, token, peliculas):
    """Test para eliminar una película"""
    pelicula = peliculas[0]  # Usamos la primera película creada en el fixture
    
    headers = {'Authorization': f'{token}'}
    response = client.delete(f'/api/peliculas/{pelicula.id}', headers=headers)

    assert response.status_code == 200

def test_obtener_peliculas(client, token, peliculas):
    """Test para obtener todas las películas"""
    headers = {'Authorization': f'{token}'}
    response = client.get('/api/peliculas', headers=headers)

    assert response.status_code == 200
