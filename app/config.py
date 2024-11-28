import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Configuración general para la aplicación.

    Esta clase contiene los parámetros de configuración comunes para el entorno de producción.
    Los valores de las variables de entorno se cargan desde un archivo `.env` utilizando la biblioteca `dotenv`.

    Atributos:
    - SECRET_KEY (str): Clave secreta utilizada para la seguridad de la aplicación. Si no está definida en el entorno, se utiliza un valor por defecto ('fallback_secret_key').
    - SQLALCHEMY_DATABASE_URI (str): URI de la base de datos de SQLAlchemy, obtenida desde la variable de entorno `DATABASE_URL`.
    - SQLALCHEMY_TRACK_MODIFICATIONS (bool): Desactiva el seguimiento de modificaciones para evitar el uso innecesario de memoria. Está configurado como `False`.
    - TOKEN_EXPIRATION_MINUTES (int): Tiempo de expiración del token en minutos para la autenticación, configurado por defecto en 30 minutos.
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TOKEN_EXPIRATION_MINUTES = 30  

class TestingConfig(Config):
    """
    Configuración para el entorno de pruebas.

    Esta clase hereda de la clase `Config` y sobrecarga ciertos parámetros para habilitar la configuración específica del entorno de pruebas.

    Atributos:
    - SQLALCHEMY_DATABASE_URI (str): URI de la base de datos utilizada para pruebas, obtenida de la variable de entorno `DATABASE_URL`.
    - TESTING (bool): Indicador para activar el modo de pruebas, configurado como `True` para simular un entorno de pruebas.
    """
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    TESTING = True