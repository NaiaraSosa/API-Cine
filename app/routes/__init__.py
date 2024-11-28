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
