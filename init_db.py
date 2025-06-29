#!/usr/bin/env python3
"""
Script para inicializar o banco de dados do sistema de gerenciamento de pacientes.
"""

import os
from app import app, db

def init_database():
    """Inicializa o banco de dados criando todas as tabelas."""
    with app.app_context():
        # Ensure the directory for the database exists
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
        
        # Create upload directory
        upload_dir = app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        # Create all tables
        db.create_all()
        
        print("Banco de dados inicializado com sucesso!")
        print(f"Diretorio de uploads criado: {upload_dir}")
        print("Sistema pronto para uso!")

if __name__ == '__main__':
    init_database()