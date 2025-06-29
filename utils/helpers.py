import re
import unicodedata
from werkzeug.utils import secure_filename
import os

def normalize_text(text):
    if not text:
        return ''
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    return text.lower()

def save_uploaded_file(file, upload_folder):
    if not file:
        return None
    filename = secure_filename(file.filename)
    file.save(os.path.join(upload_folder, filename))
    return filename

def validate_cpf(cpf):
    if not cpf or len(cpf) != 11:
        return False
    return True

def format_cpf(cpf):
    if not cpf:
        return ""
    return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'

def format_phone(phone):
    if not phone:
        return ""
    return f'({phone[:2]}) {phone[2:7]}-{phone[7:]}'

def clean_numeric_input(input_str):
    if not input_str:
        return ""
    return re.sub(r'\D', '', input_str)