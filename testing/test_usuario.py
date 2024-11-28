import pytest
from app.models.usuario import Usuario
from app.models.rol import Rol

''' Test para editar usuario por ID '''
def test_editar_usuario(client, token, usuario):
    usuario_creado, usuario_2 = usuario
    usuario_id = usuario_creado.id  

    data = {
        'nombre': 'Juanito',
        'apellido': 'Pérez González',
        'correo_electronico': 'juanito.perez@example.com',
        'fecha_nacimiento': '02-02-1999',
        'contraseña': 'nueva1',  
        'id_rol': 1  
    }

    headers = {'Authorization': f'{token}'}
    
    response = client.put(f'/api/usuarios/{usuario_id}', json=data, headers=headers)

    assert response.status_code == 200
    
    
''' Test para obtener usuario por ID '''
def test_obtener_usuario_por_id(client, token, usuario):
    usuario_creado, usuario_1 = usuario
    usuario_id = usuario_1.id 

    headers = {'Authorization': f'{token}'} 
    
    response = client.get(f'/api/usuarios/{usuario_id}', headers=headers)

    assert response.status_code == 200
    
    
'''Test para obtener todos los usuarios'''
def test_obtener_usuarios(client, token):
    headers = {'Authorization': f'{token}'}

    response = client.get('/api/usuarios', headers=headers)

    assert response.status_code == 200
    
    
'''Test para eliminar un usuario por ID'''
def test_eliminar_usuario(client, token, usuario):
    usuario_creado, usuario_2 = usuario
    usuario_id = usuario_creado.id

    headers = {'Authorization': f'{token}'}  

    response = client.delete(f'/api/usuarios/{usuario_id}', headers=headers)


    assert response.status_code == 200


