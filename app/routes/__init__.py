from .usuario_routes import usuario_bp
from .pelicula_routes import pelicula_bp
from .sala_routes import sala_bp 
from .funcion_routes import funcion_bp
from .rol_routes import rol_bp
from .clasificacion_routes import clasificacion_bp
from .metodo_pago_routes import metodo_pago_bp
from .entrada_routes import entrada_bp
from .configuracion_routes import config_bp
from .reseña_routes import reseña_bp
from .producto_routes import producto_bp

def register_blueprints(app):
    """
    Registra todos los blueprints de la aplicación.

    Esta función se encarga de registrar los diferentes blueprints de rutas (definidos en otros módulos),
    permitiendo que las rutas de cada uno de los componentes de la aplicación estén disponibles dentro de 
    la aplicación Flask. Cada blueprint se registra con el prefijo '/api' para organizar las rutas y 
    crear una API RESTful.

    Parámetros:
        app (Flask): La instancia de la aplicación Flask que se va a configurar con los blueprints.

    Rutas registradas:
        - /api/usuario: Rutas relacionadas con los usuarios.
        - /api/pelicula: Rutas relacionadas con las películas.
        - /api/sala: Rutas relacionadas con las salas de cine.
        - /api/funcion: Rutas relacionadas con las funciones de cine.
        - /api/rol: Rutas relacionadas con los roles de los usuarios.
        - /api/clasificacion: Rutas relacionadas con las clasificaciones de películas.
        - /api/metodo_pago: Rutas relacionadas con los métodos de pago.
        - /api/entrada: Rutas relacionadas con las entradas de cine.
        - /api/configuracion: Rutas relacionadas con la configuración de la aplicación.
        - /api/reseña: Rutas relacionadas con las reseñas de las películas.
        - /api/producto: Rutas relacionadas con los productos (como snacks o bebidas) disponibles para la venta.
    """
    app.register_blueprint(usuario_bp, url_prefix='/api')
    app.register_blueprint(pelicula_bp, url_prefix='/api')
    app.register_blueprint(sala_bp, url_prefix='/api')
    app.register_blueprint(funcion_bp, url_prefix='/api')
    app.register_blueprint(rol_bp, url_prefix='/api')
    app.register_blueprint(producto_bp, url_prefix='/api')
    app.register_blueprint(clasificacion_bp, url_prefix='/api')
    app.register_blueprint(metodo_pago_bp, url_prefix='/api')
    app.register_blueprint(entrada_bp, url_prefix='/api')
    app.register_blueprint(config_bp, url_prefix='/api')
    app.register_blueprint(reseña_bp, url_prefix='/api')
