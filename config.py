import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una-clave-secreta-muy-dificil'
    # Conexión a la base de datos PostgreSQL que crearemos con Docker
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:mysecretpassword@localhost:5432/diagnovet'
    SQLALCHEMY_TRACK_MODIFICATIONS = False