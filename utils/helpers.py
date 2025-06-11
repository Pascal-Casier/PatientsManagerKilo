import os
import re
from werkzeug.utils import secure_filename
from PIL import Image
from flask import current_app

def allowed_file(filename):
    """Verifica se o arquivo tem uma extensão permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_uploaded_file(file, upload_folder):
    """Salva arquivo enviado e retorna o caminho"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        # Criar nome único para evitar conflitos
        name, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(os.path.join(upload_folder, filename)):
            filename = f"{name}_{counter}{ext}"
            counter += 1
        
        filepath = os.path.join(upload_folder, filename)
        
        # Criar diretório se não existir
        os.makedirs(upload_folder, exist_ok=True)
        
        # Salvar arquivo
        file.save(filepath)
        
        # Redimensionar imagem se necessário
        try:
            with Image.open(filepath) as img:
                # Redimensionar para máximo 800x600 mantendo proporção
                img.thumbnail((800, 600), Image.Resampling.LANCZOS)
                img.save(filepath, optimize=True, quality=85)
        except Exception as e:
            print(f"Erro ao processar imagem: {e}")
        
        return filename
    return None

def validate_cpf(cpf):
    """Valida CPF brasileiro"""
    # Remove caracteres não numéricos
    cpf = re.sub(r'[^0-9]', '', cpf)
    
    # Verifica se tem 11 dígitos
    if len(cpf) != 11:
        return False
    
    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False
    
    # Calcula primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    # Calcula segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    # Verifica se os dígitos calculados conferem
    return cpf[-2:] == f"{digito1}{digito2}"

def format_cpf(cpf):
    """Formata CPF para exibição"""
    cpf = re.sub(r'[^0-9]', '', cpf)
    if len(cpf) == 11:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return cpf

def format_phone(phone):
    """Formata telefone para exibição"""
    phone = re.sub(r'[^0-9]', '', phone)
    if len(phone) == 11:
        return f"({phone[:2]}) {phone[2:7]}-{phone[7:]}"
    elif len(phone) == 10:
        return f"({phone[:2]}) {phone[2:6]}-{phone[6:]}"
    return phone

def clean_numeric_input(value):
    """Remove caracteres não numéricos de uma string"""
    return re.sub(r'[^0-9]', '', value) if value else ''