from .usuario_routes import usuario_bp
from .pelicula_routes import pelicula_bp
from .sala_routes import sala_bp 
from .funcion_routes import funcion_bp
from .promocion_routes import promocion_bp

def register_blueprints(app):
    app.register_blueprint(usuario_bp, url_prefix='/api')
    app.register_blueprint(pelicula_bp, url_prefix='/api')
    app.register_blueprint(sala_bp, url_prefix='/api')
    app.register_blueprint(funcion_bp, url_prefix='/api')
    app.register_blueprint(promocion_bp, url_prefix='/api')