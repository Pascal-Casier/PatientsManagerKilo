import os
from datetime import timedelta
import sys

class Config:
    # Configurações básicas
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Configurações do banco de dados
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        # Running in a PyInstaller bundle
        APP_DATA_DIR = os.path.join(os.path.expanduser('~'), '.PatientManagerKilo')
        os.makedirs(APP_DATA_DIR, exist_ok=True)
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(APP_DATA_DIR, "database.db")}'
        UPLOAD_FOLDER = os.path.join(APP_DATA_DIR, 'uploads')
    else:
        # Running in development mode
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{os.path.join(BASE_DIR, "database", "database.db")}'
        UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações de upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Configurações de sessão
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Configurações de formulário
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None