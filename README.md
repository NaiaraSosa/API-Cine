# CINEPI

## Descripción
CINEPI es una API diseñada para gestionar un cine, donde los usuarios pueden ver películas, comprar entradas, gestionar sus perfiles y dejar reseñas. 

## Requisitos
- Python 3.8 o superior
- pip (gestor de paquetes)
- PostgreSQL (Gestor de base de datos)
- Flask (para el servidor web)
- Flask-SQLAlchemy (ORM para la base de datos)

## Instalación

1. Clonar el repositorio
   
   `git clone https://github.com/usuario/API-Cine.git`
   
   `cd API-Cine`

3. Crear un entorno virtual (opcional pero recomendado)
   python -m venv .venv
   source .venv/bin/activate  # En Windows usa `.venv\Scripts\activate`

4. Instalar dependencias
   pip install -r requirements.txt

5. Configuración de la base de datos
   Asegurate de tener PostgreSQL instalado y configurado, y crear una base de datos con el nombre "cine".

6. Configuración del entorno
   Crea un archivo .env en la raíz del proyecto y agrega las siguientes variables:
   DATABASE_URL = postgresql://usuario:contraseña@localhost/cine
   SECRET_KEY = tu_contraseña
   MAIL_USERNAME=tu_mail@gmail.com
   MAIL_PASSWORD=contraseñ_mail
   MAIL_DEFAULT_SENDER=tu_mail@gmail.com

7. Ejecutar la API localmente
   flask run
   La API estará corriendo en http://127.0.0.1:5000/


