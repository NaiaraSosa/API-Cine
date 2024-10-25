from flask import Flask, flash, redirect, request, session, url_for, jsonify
import os
from supabase import create_client, Client
from werkzeug.security import generate_password_hash, check_password_hash

# Supabase URL y clave de API que proporciona Supabase
SUPABASE_URL = "https://tnpezlywonvekopfyvtz.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRucGV6bHl3b252ZWtvcGZ5dnR6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjk3OTUxMzMsImV4cCI6MjA0NTM3MTEzM30.TCOJiz-jI9FJidr23LpTt2g207vvj7ZAc1zVzveKt5c"

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(12)  # Clave secreta para la sesión

    # Crear cliente de Supabase
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    # Ruta principal
    @app.route('/')
    def home():
        if not session.get('logged_in'):
            return jsonify({"message": "No estas logueado"}), 401  # Respuesta cuando no se está logueado
        else:
            return jsonify({"message": "Bienvenido a API-CINE!"}), 200



    # Ruta para registrar un nuevo usuario
    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        print(data)
        nombre_usuario = data.get('nombre_usuario')
        correo_electronico = data.get('correo_electronico')
        contraseña = data.get('contraseña')

        if not nombre_usuario or not correo_electronico or not contraseña:
            return jsonify({"error": "Completar correctamente todos los campos."}), 400

        # Encriptar la contraseña antes de guardarla
        contraseña_hashed = generate_password_hash(contraseña)

        # Insertar el usuario en la base de datos usando Supabase
        try:
            response = supabase.table('Usuarios').insert({
                "nombre_usuario": nombre_usuario,
                "correo_electronico": correo_electronico,
                "contraseña": contraseña_hashed
            }).execute()
            return jsonify({"message": "Usuario registrado exitosamente!"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Ruta para el login
    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        nombre_usuario = data.get('nombre_usuario')
        correo_electronico = data.get('correo_electronico')
        contraseña = data.get('contraseña')

        if not nombre_usuario or not correo_electronico or not contraseña:
            return jsonify({"error": "Completar correctamente todos los campos."}), 400


        # Buscar el usuario en la base de datos
        user = supabase.table('Usuarios').select('*').eq('nombre_usuario', nombre_usuario).execute()

        if user.data:
            stored_password = user.data[0]['contraseña']
            if check_password_hash(stored_password, contraseña):
                session['logged_in'] = True
                return jsonify({"message": "Se ha logueado exitosamente!"}), 200
            else:
                return jsonify({"error": "Contraseña incorrecta."}), 401
        else:
            return jsonify({"error": "Usuario no registrado."}), 404
    
    # Ruta para hacer logout
    @app.route('/logout', methods=['POST'])
    def logout():
        session['logged_in'] = False
        return jsonify({"message": "Se ha deslogueado exitosamente!"}), 200

    return app


if __name__ == "__main__":
    app = create_app()  # Crea la instancia de la aplicación
    app.run(debug=True, host='0.0.0.0', port=4000)