import pytest
from app import create_app
from app.connection import db
from datetime import datetime, timedelta
from sqlalchemy.sql import text
from app.models import Rol, Usuario, Entrada, Funcion, TransaccionEntrada, Clasificacion, MetodoPago, Pelicula, Sala, Reseña, Producto, Configuracion, TransaccionProductos, DetalleTransaccionProducto

''' Configuracion de base de datos para pruebas '''
@pytest.fixture(scope='function')
def client():
    app = create_app('testing')
    
    '''Creamos las tablas y algunos registros necesarios'''
    with app.test_client() as client:
        with app.app_context():
            db.create_all()

            roles_requeridos = ['Administrador', 'Cliente']
            roles_existentes = {rol.nombre for rol in Rol.query.all()}

            for rol in roles_requeridos:
                if rol not in roles_existentes:
                    db.session.add(Rol(nombre=rol))
            
            clasificaciones_existentes = Clasificacion.query.all()
            clasificaciones_requeridas = ['ATP', 'PG13', 'PG18']
            codigos_existentes = {c.codigo for c in clasificaciones_existentes}

            for clasificacion in clasificaciones_requeridas:
                if clasificacion not in codigos_existentes:
                    db.session.add(Clasificacion(codigo=clasificacion))
                    
                    
            configuraciones_requeridas = [
                {'clave': 'precio_entrada', 'valor': '100.00'},
            ]
            
            claves_existentes = {config.clave for config in Configuracion.query.all()}
            for config in configuraciones_requeridas:
                if config['clave'] not in claves_existentes:
                    db.session.add(Configuracion(clave=config['clave'], valor=config['valor']))

            db.session.commit()
        yield client

        
    '''Eliminamos los registros y reiniciamos los ID al final de la prueba, respetando las dependencias'''
    with app.app_context():

        db.session.execute(text('TRUNCATE TABLE reseña RESTART IDENTITY CASCADE;'))
        db.session.execute(text('TRUNCATE TABLE transaccion_entrada RESTART IDENTITY CASCADE;'))
        db.session.execute(text('TRUNCATE TABLE entrada RESTART IDENTITY CASCADE;'))
        db.session.execute(text('TRUNCATE TABLE usuario RESTART IDENTITY CASCADE;'))
        db.session.execute(text('TRUNCATE TABLE metodo_pago RESTART IDENTITY CASCADE;'))
        db.session.execute(text('TRUNCATE TABLE funcion RESTART IDENTITY CASCADE;'))
        db.session.execute(text('TRUNCATE TABLE pelicula RESTART IDENTITY CASCADE;'))
        db.session.execute(text('TRUNCATE TABLE transaccion_productos RESTART IDENTITY CASCADE;'))
        db.session.commit()     
        db.session.execute(text('TRUNCATE TABLE detalle_transaccion_producto RESTART IDENTITY CASCADE;'))
        db.session.execute(text('TRUNCATE TABLE clasificacion RESTART IDENTITY CASCADE;'))
        db.session.execute(text('TRUNCATE TABLE sala RESTART IDENTITY CASCADE;'))
        db.session.execute(text('TRUNCATE TABLE producto RESTART IDENTITY CASCADE;'))
        db.session.execute(text('TRUNCATE TABLE rol RESTART IDENTITY CASCADE;'))

        db.session.commit()
    
''' Fixture para crear usuarios  '''        
@pytest.fixture(scope='function')
def usuario(client):
    data = {
        'nombre': 'Juan',
        'apellido': 'Pérez',
        'correo_electronico': 'juan.perez@gmail.com',
        'fecha_nacimiento': '02-02-1990',
        'contraseña': 'pas123',  
        'id_rol': 1
    }
    
    data_1 = {
        'nombre': 'Maria',
        'apellido': 'Gómez',
        'correo_electronico': 'maria.gomez@gmail.com',
        'fecha_nacimiento': '02-02-1999',
        'contraseña': 'pas456',  
        'id_rol': 1
    }

    response = client.post('/api/usuarios', json=data)
    assert response.status_code == 201  
    usuario_creado = Usuario.query.filter_by(correo_electronico=data['correo_electronico']).first()
    assert usuario_creado is not None  
    
    response_1 = client.post('/api/usuarios', json=data_1)
    assert response_1.status_code == 201  
    usuario_1 = Usuario.query.filter_by(correo_electronico=data_1['correo_electronico']).first()
    assert usuario_1 is not None 
    
    print(usuario_creado)
    return [usuario_creado, usuario_1] 

''' Fixture para hacer un login y conseguir el token '''
@pytest.fixture
def token(client, usuario):
    login_data = {
        'correo_electronico': 'juan.perez@gmail.com',
        'contraseña': 'pas123'
    }

    login_response = client.post('/api/login', json=login_data)
    

    assert login_response.status_code == 200

    token = login_response.json.get('token')
    
    assert token is not None
    print(token)
    
    return token  

''' Fixture para crear roles '''
@pytest.fixture
def rol(client, token):
    data = {'nombre': 'Editor'}
    
    headers = {'Authorization': f'{token}'}

    response = client.post('/api/roles', json=data, headers=headers)

    assert response.status_code == 201
    
    nuevo_rol = Rol.query.filter_by(nombre='Editor').first()
    assert nuevo_rol is not None
    
    return nuevo_rol

''' Fixture para crear clasificaciones'''
@pytest.fixture
def clasificacion(client, token):
    data = {'codigo': 'ABC123'}
    
    headers = {'Authorization': f'{token}'}
    
    response = client.post('/api/clasificaciones', json=data, headers=headers)

    assert response.status_code == 201 
    
    clasificacion_creada = Clasificacion.query.filter_by(codigo=data['codigo']).first()
    assert clasificacion_creada is not None 
    
    return clasificacion_creada

''' Fixture para crear metdos de pago '''
@pytest.fixture
def metodos_pago(client, token):
    data_1 = {'tipo': 'Tarjeta de Crédito'}
    data_2 = {'tipo': 'PayPal'}

    headers = {'Authorization': f'{token}'}

    response_1 = client.post('/api/metodos_pago', json=data_1, headers=headers)
    response_2 = client.post('/api/metodos_pago', json=data_2, headers=headers)

    assert response_1.status_code == 201
    assert response_2.status_code == 201

    metodo_pago_1 = MetodoPago.query.filter_by(tipo=data_1['tipo']).first()
    metodo_pago_2 = MetodoPago.query.filter_by(tipo=data_2['tipo']).first()

    
    return metodo_pago_1, metodo_pago_2

''' Fixture para crear peliculas '''
@pytest.fixture
def peliculas(client, token, clasificacion):
    headers = {'Authorization': f'{token}'}

    data_1 = {
        'titulo': 'Pelicula 1', 
        'director': 'Director 1', 
        'duracion': 120, 
        'id_clasificacion': clasificacion.id,  
        'sinopsis': 'Sinopsis de la pelicula 1'
    }
    
    data_2 = {
        'titulo': 'Pelicula 2', 
        'director': 'Director 2', 
        'duracion': 110, 
        'id_clasificacion': clasificacion.id, 
        'sinopsis': 'Sinopsis de la pelicula 2'
    }

    response_1 = client.post('/api/peliculas', json=data_1, headers=headers)
    response_2 = client.post('/api/peliculas', json=data_2, headers=headers)

    assert response_1.status_code == 201
    assert response_2.status_code == 201

    pelicula_1 = Pelicula.query.filter_by(titulo=data_1['titulo']).first()
    pelicula_2 = Pelicula.query.filter_by(titulo=data_2['titulo']).first()



    return [pelicula_1, pelicula_2]

''' Fixture para crear salas '''
@pytest.fixture
def salas(client, token):
    headers = {'Authorization': f'{token}'}

    data_1 = {'nombre': 'Sala 1', 'capacidad': 100}
    data_2 = {'nombre': 'Sala 2', 'capacidad': 150}

    response_1 = client.post('/api/salas', json=data_1, headers=headers)
    response_2 = client.post('/api/salas', json=data_2, headers=headers)

    assert response_1.status_code == 201
    assert response_2.status_code == 201

    sala_1 = Sala.query.filter_by(nombre=data_1['nombre']).first()
    sala_2 = Sala.query.filter_by(nombre=data_2['nombre']).first()

    return [sala_1, sala_2]

''' Fixture para crear reseñas '''
@pytest.fixture
def reseñas(client, token, peliculas, usuario):
    headers = {'Authorization': f'{token}'}
    usuario_creado, usuario_1 = usuario
    pelicula1, pelicula2 = peliculas

    data_1 = {
        'id_usuario': usuario_creado.id,
        'id_pelicula': pelicula1.id,
        'calificacion': 4,
        'comentario': "Buena pelicula, me gusto mucho."
    }
    
    data_2 = {
        'id_usuario': usuario_1.id,
        'id_pelicula': pelicula2.id,
        'calificacion': 3,
        'comentario': "La pelicula estuvo bien, pero esperaba mas."
    }

    response_1 = client.post('/api/reseñas', json=data_1, headers=headers)
    response_2 = client.post('/api/reseñas', json=data_2, headers=headers)

    assert response_1.status_code == 201
    assert response_2.status_code == 201

    reseña_1 = Reseña.query.filter_by(id_usuario=usuario_creado.id).first()
    reseña_2 = Reseña.query.filter_by(id_usuario=usuario_1.id).first()


    return [reseña_1, reseña_2]

''' Fixture para crear funciones '''
@pytest.fixture
def funciones(client, token, peliculas, salas):
    headers = {'Authorization': f'{token}'}
    pelicula1, pelicula2 = peliculas
    sala1, sala2 = salas

    data_1 = {
        'id_pelicula': pelicula1.id,
        'id_sala': sala1.id,
        'horario_inicio': '2024-12-01T18:00:00',
        'horario_fin': '2024-12-01T20:00:00'
    }

    data_2 = {
        'id_pelicula': pelicula2.id,
        'id_sala': sala2.id,
        'horario_inicio': '2024-12-02T15:00:00',
        'horario_fin': '2024-12-02T17:00:00'
    }

    response_1 = client.post('/api/funciones', json=data_1, headers=headers)
    response_2 = client.post('/api/funciones', json=data_2, headers=headers)

    assert response_1.status_code == 201
    assert response_2.status_code == 201

    funcion_1 = Funcion.query.filter_by(id_pelicula=pelicula1.id).first()
    funcion_2 = Funcion.query.filter_by(id_pelicula=pelicula2.id).first()

    return [funcion_1, funcion_2]

''' Fixture para crear productos '''
@pytest.fixture
def productos(client, token):
    headers = {'Authorization': f'{token}'}

    data_1 = {'nombre': 'Producto 1', 'precio': 100.00}
    data_2 = {'nombre': 'Producto 2', 'precio': 150.50}

    response_1 = client.post('/api/productos', json=data_1, headers=headers)
    response_2 = client.post('/api/productos', json=data_2, headers=headers)

    assert response_1.status_code == 201
    assert response_2.status_code == 201

    producto_1 = Producto.query.filter_by(nombre=data_1['nombre']).first()
    producto_2 = Producto.query.filter_by(nombre=data_2['nombre']).first()


    return [producto_1, producto_2]

''' Fixture para crear transacciones de entrada '''
@pytest.fixture
def transacciones_entrada(client, usuario, metodos_pago, funciones):
    usuario = usuario[0]
    metodopago = metodos_pago[0]
    funcion = funciones[0]

    data = {
        'id_usuario': usuario.id,
        'id_funcion': funcion.id,
        'cantidad_entradas': 2,
        'total': 200.00,  # Total: 2 entradas * 100.00
        'id_metodo_pago': metodopago.id,
        'fecha': '2024-11-27T12:00:00'
    }

    response = client.post('/api/transacciones_entrada', json=data)

    assert response.status_code == 201

    transaccion = TransaccionEntrada.query.filter_by(id_usuario=usuario.id).first()


    return transaccion

''' Fixture para crear entradas '''
@pytest.fixture
def entradas(client, funciones, transacciones_entrada):
    headers = {'Authorization': f'{token}'}
    funcion1, funcion2 = funciones
    transaccion = transacciones_entrada

    data_1 = {'id_funcion': funcion1.id, 'id_transaccion': transaccion.id}
    data_2 = {'id_funcion': funcion2.id, 'id_transaccion': transaccion.id}

    response_1 = client.post('/api/entradas', json=data_1, headers=headers)
    response_2 = client.post('/api/entradas', json=data_2, headers=headers)

    assert response_1.status_code == 201
    assert response_2.status_code == 201

    entrada_1 = Entrada.query.filter_by(id_transaccion=transaccion.id).first()
    entrada_2 = Entrada.query.filter_by(id_transaccion=transaccion.id).first()

    return [entrada_1, entrada_2]