# CINEPI

## Descripción
CINEPI es una API diseñada para gestionar un cine, donde los usuarios pueden ver películas, comprar entradas y productos, gestionar sus perfiles y dejar reseñas. 

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
   
   `python -m venv .venv`
   
   source .venv/bin/activate  # En Windows usa `.venv\Scripts\activate`

5. Instalar dependencias
   
   `pip install -r requirements.txt`

7. Configuración de la base de datos
   
   Asegurate de tener PostgreSQL instalado y configurado, y crear una base de datos con el nombre "cine".

9. Configuración del entorno
    
   Crea un archivo `.env` en la raíz del proyecto y agrega las siguientes variables:
   
   DATABASE_URL = postgresql://usuario:contraseña@localhost/cine
   
   SECRET_KEY = tu_contraseña
   

11. Ejecutar la API localmente
    
    `flask run`
    La API estará corriendo en `http://127.0.0.1:5000/`


