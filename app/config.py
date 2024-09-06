import os

SECRET_KEY = 'secret-key'
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:password@db:5432/carford_db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
