from .usuario_routes import usuario_bp
from .pelicula_routes import pelicula_bp

def register_blueprints(app):
    app.register_blueprint(usuario_bp, url_prefix='/api')
    app.register_blueprint(pelicula_bp, url_prefix='/api')
