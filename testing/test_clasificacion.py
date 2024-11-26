import pytest
from app.models.clasificacion import Clasificacion


def test_obtener_clasificacion(client, token, clasificacion):
    clasificacion_id = clasificacion.id
    """Test para obtener una clasificación por ID"""

    # Headers con el token para autenticación
    headers = {'Authorization': f'{token}'}

    # Realiza la solicitud GET para obtener la clasificación por ID
    response = client.get(f'/api/clasificaciones/{clasificacion_id}', headers=headers)

    # Verifica que la respuesta sea 200 (éxito)
    assert response.status_code == 200




def test_obtener_clasificaciones(client, token):
    """Test para obtener todas las clasificaciones"""

    # Headers con el token para autenticación
    headers = {'Authorization': f'{token}'}

    # Realiza la solicitud GET para obtener todas las clasificaciones
    response = client.get('/api/clasificaciones', headers=headers)

    # Verifica que la respuesta sea 200 (éxito)
    assert response.status_code == 200


def test_editar_clasificacion(client, token, clasificacion):
    """Test para editar una clasificación existente"""
    clasificacion_id = clasificacion.id
    data = {'codigo': 'pg25'}
    # Headers con el token para autenticación
    headers = {'Authorization': f'{token}'}

    # Realiza la solicitud PUT para editar la clasificación
    response = client.put(f'/api/clasificaciones/{clasificacion_id}', json=data, headers=headers)

    # Verifica que la respuesta sea 200 (éxito)
    assert response.status_code == 200



def test_eliminar_clasificacion(client, token, clasificacion):
    """Test para eliminar una clasificación"""
    clasificacion_id = clasificacion.id
    # Headers con el token para autenticación
    headers = {'Authorization': f'{token}'}

    # Realiza la solicitud DELETE para eliminar la clasificación
    response = client.delete(f'/api/clasificaciones/{clasificacion_id}', headers=headers)

    # Verifica que la respuesta sea 200 (éxito)
    assert response.status_code == 200

