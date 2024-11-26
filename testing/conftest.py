import pytest
from app import create_app
from app.connection import db
from app.models import Rol, Usuario, Entrada, Funcion, Transaccion, Clasificacion, MetodoPago, Pelicula, Sala

# Configuración de la base de datos de pruebas
@pytest.fixture(scope='function')
def client():
    app = create_app('testing')

    with app.test_client() as client:
        with app.app_context():
            # Crea las tablas solo si no existen
            db.create_all()

            # Configura los roles necesarios
            if not Rol.query.get(1):
                db.session.add(Rol(id=1, nombre='Administrador'))
            if not Rol.query.get(2):
                db.session.add(Rol(id=2, nombre='Cliente'))
            db.session.commit()

        yield client

        with app.app_context():
    # Limpia primero las tablas con dependencias
    db.session.execute('TRUNCATE TABLE reseña RESTART IDENTITY CASCADE;')
    db.session.execute('TRUNCATE TABLE entrada RESTART IDENTITY CASCADE;')
    db.session.execute('TRUNCATE TABLE transaccion RESTART IDENTITY CASCADE;')
    db.session.execute('TRUNCATE TABLE usuario RESTART IDENTITY CASCADE;')
    db.session.execute('TRUNCATE TABLE funcion RESTART IDENTITY CASCADE;')
    db.session.execute('TRUNCATE TABLE pelicula RESTART IDENTITY CASCADE;')
    db.session.commit()

    # Limpia el resto de las tablas
    
    db.session.execute('TRUNCATE TABLE clasificacion RESTART IDENTITY CASCADE;')
    db.session.execute('TRUNCATE TABLE sala RESTART IDENTITY CASCADE;')
    db.session.execute('TRUNCATE TABLE metodo_pago RESTART IDENTITY CASCADE;')
    db.session.execute('TRUNCATE TABLE promocion RESTART IDENTITY CASCADE;')
    db.session.execute('TRUNCATE TABLE producto RESTART IDENTITY CASCADE;')
    db.session.execute('TRUNCATE TABLE rol RESTART IDENTITY CASCADE;')
    db.session.commit()
            
@pytest.fixture(scope='function')
def usuario(client):
    """Fixture para crear un usuario y devolverlo con todos sus datos"""
    data = {
        'nombre': 'Juan',
        'apellido': 'Pérez',
        'correo_electronico': 'juan.perez@example.com',
        'fecha_nacimiento': '1990-01-01',
        'contraseña': 'pas123',  # Contraseña válida
        'id_rol': 1
    }
    
    data_1 = {
        'nombre': 'Maria',
        'apellido': 'Gómez',
        'correo_electronico': 'maria.gomez@example.com',
        'fecha_nacimiento': '1985-02-02',
        'contraseña': 'pas456',  # Contraseña válida
        'id_rol': 1
    }

    response = client.post('/api/usuarios', json=data)
    assert response.status_code == 201  # Asegúrate de que el usuario se creó correctamente
    usuario_creado = Usuario.query.filter_by(correo_electronico=data['correo_electronico']).first()
    assert usuario_creado is not None  # Verifica que el usuario existe
    
    response_1 = client.post('/api/usuarios', json=data_1)
    assert response_1.status_code == 201  # Asegúrate de que el primer usuario se creó correctamente
    usuario_1 = Usuario.query.filter_by(correo_electronico=data_1['correo_electronico']).first()
    assert usuario_1 is not None  # Verifica que el usuario 1 existe
    
    print(usuario_creado)
    return usuario_creado, usuario_1  # Devuelve el usuario creado con todos sus datos


@pytest.fixture
def token(client, usuario):
    """Fixture que obtiene el token de autenticación después de hacer login con el usuario creado."""
    
    # Datos para hacer login con el usuario
    login_data = {
        'correo_electronico': 'juan.perez@example.com',
        'contraseña': 'pas123'
    }

    # Realizar el login
    login_response = client.post('/api/login', json=login_data)
    
    # Asegurarse de que el login fue exitoso
    assert login_response.status_code == 200
    
    # Obtener el token del cuerpo de la respuesta
    token = login_response.json.get('token')
    
    # Verificar que el token esté presente
    assert token is not None
    print(token)
    
    return token  # Devolver el token para ser usado en otros tests

@pytest.fixture
def rol(client, token):
    """Fixture para crear un rol en la base de datos antes de los tests"""
    # Datos para el nuevo rol
    data = {'nombre': 'Editor'}
    
    # Headers con el token para autenticación
    headers = {'Authorization': f'{token}'}
    
    # Realiza la solicitud POST para agregar el rol
    response = client.post('/api/roles', json=data, headers=headers)

    # Verifica que la respuesta sea 201 (creado)
    assert response.status_code == 201
    assert response.json['message'] == 'Rol agregado exitosamente'
    
    # Obtener el rol de la base de datos para usarlo en los tests
    nuevo_rol = Rol.query.filter_by(nombre='Editor').first()
    assert nuevo_rol is not None
    
    return nuevo_rol

@pytest.fixture
def clasificacion(client, token):
    """Fixture para crear una clasificación y devolverla con todos sus datos"""
    
    # Datos para la nueva clasificación
    data = {'codigo': 'ABC123'}
    
    # Headers con el token para autenticación
    headers = {'Authorization': f'{token}'}
    
    # Realiza la solicitud POST para agregar la clasificación
    response = client.post('/api/clasificaciones', json=data, headers=headers)
    
    # Verifica que la clasificación se haya creado correctamente
    assert response.status_code == 201  # Asegúrate de que la clasificación se haya creado
    
    # Obtiene la clasificación recién creada desde la base de datos
    clasificacion_creada = Clasificacion.query.filter_by(codigo=data['codigo']).first()
    assert clasificacion_creada is not None  # Verifica que la clasificación exista
    
    # Devuelve la clasificación creada para su uso en otros tests
    return clasificacion_creada

@pytest.fixture
def metodos_pago(client, token):
    """Fixture para crear dos métodos de pago y devolverlos"""

    # Datos para los dos métodos de pago
    data_1 = {'tipo': 'Tarjeta de Crédito'}
    data_2 = {'tipo': 'PayPal'}

    # Headers con el token para autenticación
    headers = {'Authorization': f'{token}'}

    # Realiza las solicitudes POST para agregar los dos métodos de pago
    response_1 = client.post('/api/metodos_pago', json=data_1, headers=headers)
    response_2 = client.post('/api/metodos_pago', json=data_2, headers=headers)

    # Verifica que ambos métodos de pago se hayan creado correctamente
    assert response_1.status_code == 201
    assert response_2.status_code == 201

    # Obtiene los métodos de pago recién creados desde la base de datos
    metodo_pago_1 = MetodoPago.query.filter_by(tipo=data_1['tipo']).first()
    metodo_pago_2 = MetodoPago.query.filter_by(tipo=data_2['tipo']).first()

    # Verifica que ambos métodos de pago existan
    assert metodo_pago_1 is not None
    assert metodo_pago_2 is not None

    # Devuelve ambos métodos de pago para su uso en los tests
    return metodo_pago_1, metodo_pago_2

''' Fixture para crear dos peliculas '''
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


''' Fixture para crear dos salas '''
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





