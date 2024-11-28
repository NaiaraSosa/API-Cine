import pytest
from app.models.entrada import Entrada
from app.models.usuario import Usuario
from app.models.funcion import  Funcion
from app.models.rol import  Rol
from app.models.metodo_pago import MetodoPago

''' Prueba para comprar entradas '''
def test_comprar_entradas(client, token, metodos_pago, funciones):  
    headers={'Authorization': f'{token}'}
    metodo_pago = metodos_pago[0]
    funcion = funciones[0]

    data = {
        'id_funcion': funcion.id,
        'cantidad': 1,
        'id_metodo_pago': metodo_pago.id
    }


    response = client.post('/api/entradas/comprar', json=data, headers = headers)
    

    assert response.status_code == 201
    




