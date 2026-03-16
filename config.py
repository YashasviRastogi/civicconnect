import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-this-in-production'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/civicconnect.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
