from app.connection import db

class Clasificacion(db.Model):
    __tablename__ = 'clasificacion'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), nullable=False)

    # relaciones
    peliculas = db.relationship("Pelicula", backref="clasificacion", lazy=True)