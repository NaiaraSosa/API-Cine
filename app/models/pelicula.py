from app.connection import db

class Pelicula(db.Model):
    __tablename__ = 'pelicula'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)  
    director = db.Column(db.String(100), nullable=False) 
    duracion = db.Column(db.Integer, nullable=False) 
    id_clasificacion = db.Column(db.Integer, db.ForeignKey('clasificacion.id'), nullable=False)
    sinopsis = db.Column(db.String(1000))  

    # relaciones
    #reseñas = db.relationship("Reseña", backref="pelicula", lazy=True)