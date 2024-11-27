import pytest
from app import create_app
from app.connection import db
from sqlalchemy.sql import text
from app.models import Rol, Usuario, Entrada, Funcion, TransaccionEntrada, Clasificacion, MetodoPago, Pelicula, Sala, Reseña, Producto, Promocion

''' Configuracion de base de datos para pruebas '''
@pytest.fixture(scope='function')
def client():
    app = create_app('testing')

''' Creamos las tablas y algunos registros necesarios '''
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

            db.session.commit()
        yield client
        
''' Eliminamos los registros y reiniciamos los ID al final de la prueba, respetando las dependencias '''
    with app.app_context():

        db.session.execute(text('TRUNCATE TABLE reseña RESTART IDENTITY CASCADE;'))
        db.session.execute(text('TRUNCATE TABLE entrada RESTART IDENTITY CASCADE;'))
        db.session.execute(text('TRUNCATE TABLE transaccion RESTART IDENTITY CASCADE;'))
        db.session.execute(text('TRUNCATE TABLE usuario RESTART IDENTITY CASCADE;'))
        db.session.execute(text('TRUNCATE TABLE funcion RESTART IDENTITY CASCADE;'))
        db.session.execute(text('TRUNCATE TABLE pelicula RESTART IDENTITY CASCADE;'))
        db.session.commit()     
        db.session.execute(text('TRUNCATE TABLE clasificacion RESTART IDENTITY CASCADE;'))
        db.session.execute(text('TRUNCATE TABLE sala RESTART IDENTITY CASCADE;'))
        db.session.execute(text('TRUNCATE TABLE metodo_pago RESTART IDENTITY CASCADE;'))
        db.session.execute(text('TRUNCATE TABLE promocion RESTART IDENTITY CASCADE;'))
        db.session.execute(text('TRUNCATE TABLE producto RESTART IDENTITY CASCADE;'))
        db.session.execute(text('TRUNCATE TABLE rol RESTART IDENTITY CASCADE;'))
        db.session.commit()
    
''' Fixture para crear usuarios  '''        
@pytest.fixture(scope='function')
def usuario(client):
    data = {
        'nombre': 'Juan',
        'apellido': 'Pérez',
        'correo_electronico': 'juan.perez@example.com',
        'fecha_nacimiento': '1990-01-01',
        'contraseña': 'pas123',  
        'id_rol': 1
    }
    
    data_1 = {
        'nombre': 'Maria',
        'apellido': 'Gómez',
        'correo_electronico': 'maria.gomez@example.com',
        'fecha_nacimiento': '1985-02-02',
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
        'correo_electronico': 'juan.perez@example.com',
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

    assert metodo_pago_1 is not None
    assert metodo_pago_2 is not None
    
    return metodo_pago_1, metodo_pago_2

''' Fixture para crear peliculas '''
@pytest.fixture
def peliculas(client, token, clasificacion):
    pelicula1 = Pelicula(
        titulo="Pelicula 1", 
        director="Director 1", 
        duracion=120, 
        id_clasificacion=clasificacion.id,  
        sinopsis="Sinopsis de la pelicula 1"
    )
    
    pelicula2 = Pelicula(
        titulo="Pelicula 2", 
        director="Director 2", 
        duracion=110, 
        id_clasificacion=clasificacion.id, 
        sinopsis="Sinopsis de la pelicula 2"
    )

    db.session.add(pelicula1)
    db.session.add(pelicula2)
    db.session.commit()

    return [pelicula1, pelicula2]

''' Fixture para crear salas '''
@pytest.fixture
def salas(client, token):
    sala1 = Sala(
        nombre="Sala 1", 
        capacidad=100
    )
    sala2 = Sala(
        nombre="Sala 2", 
        capacidad=150
    )

    db.session.add(sala1)
    db.session.add(sala2)
    db.session.commit()

    return [sala1, sala2]

''' Fixture para crear reseñas '''
@pytest.fixture
def reseñas(client, token, peliculas, usuario):
    usuario_creado, usuario_1 = usuario
    pelicula1, pelicula2 = peliculas

    reseña1 = Reseña(
        id_usuario=usuario_creado.id,
        id_pelicula=pelicula1.id,
        calificacion=4,
        comentario="Buena pelicula, me gusto mucho."
    )
    
    reseña2 = Reseña(
        id_usuario=usuario_1.id,
        id_pelicula=pelicula2.id,
        calificacion=3,
        comentario="La pelicula estuvo bien, pero esperaba mas."
    )

    db.session.add(reseña1)
    db.session.add(reseña2)
    db.session.commit()  

    assert reseña1.id is not None
    assert reseña2.id is not None

    return [reseña1, reseña2]





