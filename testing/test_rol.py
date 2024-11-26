import pytest
from app.models.rol import Rol

def test_obtener_rol(client, token, rol):
    """Test para obtener un rol por ID"""
    rol_id = rol.id
    # Headers con el token para autenticación
    headers = {'Authorization': f'{token}'}

    # Realiza la solicitud GET para obtener el rol por ID
    response = client.get(f'/api/roles/{rol_id}', headers=headers)

    # Verifica que la respuesta sea 200 (éxito)
    assert response.status_code == 200


def test_obtener_roles(client, token):

    # Headers con el token para autenticación
    headers = {'Authorization': f'{token}'}

    # Realiza la solicitud GET para obtener todos los roles
    response = client.get('/api/roles', headers=headers)

    # Verifica que la respuesta sea 200 (éxito)
    assert response.status_code == 200



def test_editar_rol(client, token, rol):
    """Test para editar un rol existente"""
    rol_id = rol.id
    # Datos para editar el rol
    data = {'nombre': 'Moderador'}

    # Headers con el token para autenticación
    headers = {'Authorization': f'{token}'}

    # Realiza la solicitud PUT para editar el rol
    response = client.put(f'/api/roles/{rol_id}', json=data, headers=headers)

    # Verifica que la respuesta sea 200 (éxito)
    assert response.status_code == 200



def test_eliminar_rol(client, token, rol):
    """Test para eliminar un rol"""
    rol_id = rol.id
    # Headers con el token para autenticación
    headers = {'Authorization': f'{token}'}

    # Realiza la solicitud DELETE para eliminar el rol
    response = client.delete(f'/api/roles/{rol_id}', headers=headers)

    # Verifica que la respuesta sea 200 (éxito)
    assert response.status_code == 200

