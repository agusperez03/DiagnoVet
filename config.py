import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una-clave-secreta-muy-dificil'

    # Lee la URL de la base de datos desde la variable de entorno
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = DATABASE_URL or 'postgresql://user:mysecretpassword@localhost:5432/diagnovet'
    SQLALCHEMY_TRACK_MODIFICATIONS = False