from flask import Flask
from flask_restful import Api, Resource

# crea instancia de Flask
app = Flask(__name__)

# crea instancia de Api
api = Api(app)

# define la clase de recurso
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

# define la ruta para el recurso
api.add_resource(HelloWorld, '/')

# ejecuta la aplicación
if __name__ == '__main__':
    app.run(debug=True)

