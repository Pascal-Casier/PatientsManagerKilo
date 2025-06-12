from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, Email, Optional, Length
from werkzeug.utils import secure_filename
from datetime import datetime, date
import os
import re

from config import Config
from database.models import db, Paciente, Tratamento
from utils.helpers import save_uploaded_file, validate_cpf, format_cpf, format_phone, clean_numeric_input

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Create upload directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Forms
class PacienteForm(FlaskForm):
    nome_completo = StringField('Nome Completo', validators=[DataRequired(), Length(min=2, max=200)])
    cpf = StringField('CPF', validators=[Optional(), Length(min=11, max=14)])
    profissao = StringField('Profissão', validators=[Optional(), Length(max=100)])
    sexo = SelectField('Sexo', choices=[('', 'Selecione...'), ('Masculino', 'Masculino'), ('Feminino', 'Feminino'), ('Outro', 'Outro')], validators=[Optional()])
    idade = IntegerField('Idade', validators=[Optional()])
    endereco = TextAreaField('Endereço', validators=[Optional(), Length(max=500)])
    telefone = StringField('Telefone', validators=[Optional(), Length(max=20)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    foto = FileField('Foto', validators=[Optional(), FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Apenas imagens são permitidas!')])
    notas = TextAreaField('Notas', validators=[Optional(), Length(max=1000)])

class TratamentoForm(FlaskForm):
    paciente_id = SelectField('Paciente', coerce=int, validators=[DataRequired()])
    queixa_principal = TextAreaField('Queixa Principal', validators=[Optional(), Length(max=500)])
    como = TextAreaField('Como?', validators=[Optional(), Length(max=500)])
    onde = TextAreaField('Onde?', validators=[Optional(), Length(max=500)])
    exames_complementares = TextAreaField('Exames Complementares', validators=[Optional(), Length(max=1000)])
    antecedentes = TextAreaField('Antecedentes', validators=[Optional(), Length(max=1000)])
    tratamentos_anteriores = TextAreaField('Tratamentos Anteriores', validators=[Optional(), Length(max=1000)])
    qualidade_sono = StringField('Qualidade do Sono', validators=[Optional(), Length(max=100)])
    movimentos = TextAreaField('Movimentos', validators=[Optional(), Length(max=500)])
    irradiacoes = TextAreaField('Irradiações', validators=[Optional(), Length(max=500)])
    conclusoes_tratamento = TextAreaField('Conclusões e Tratamento', validators=[Optional(), Length(max=1000)])
    data_retorno = DateField('Data de Retorno', validators=[Optional()])
    retorno = TextAreaField('Retorno', validators=[Optional(), Length(max=500)])

# Routes
@app.route('/')
def index():
    # Get statistics
    total_pacientes = Paciente.query.count()
    total_tratamentos = Tratamento.query.count()
    
    # Get recent activities
    pacientes_recentes = Paciente.query.order_by(Paciente.created_at.desc()).limit(5).all()
    tratamentos_recentes = Tratamento.query.order_by(Tratamento.created_at.desc()).limit(5).all()
    
    return render_template('index.html', 
                         total_pacientes=total_pacientes,
                         total_tratamentos=total_tratamentos,
                         pacientes_recentes=pacientes_recentes,
                         tratamentos_recentes=tratamentos_recentes)

@app.route('/novo-paciente', methods=['GET', 'POST'])
def novo_paciente():
    form = PacienteForm()
    
    if form.validate_on_submit():
        # Clean CPF
        cpf_clean = clean_numeric_input(form.cpf.data)

        # Check if CPF already exists
        #if cpf_clean:
        #    existing_patient = Paciente.query.filter_by(cpf=cpf_clean).first()
        #    if existing_patient:
        #        flash('Já existe um paciente cadastrado com este CPF.', 'error')
        #        return render_template('novo_paciente.html', form=form)
        
        # Handle file upload
        foto_filename = None
        if form.foto.data:
            foto_filename = save_uploaded_file(form.foto.data, app.config['UPLOAD_FOLDER'])
            if not foto_filename:
                flash('Erro ao fazer upload da foto. Verifique o formato e tamanho do arquivo.', 'error')
                return render_template('novo_paciente.html', form=form)
        
        # Create new patient
        paciente = Paciente(
            nome_completo=form.nome_completo.data.strip().title(),
            cpf=cpf_clean,
            profissao=form.profissao.data.strip() if form.profissao.data else None,
            sexo=form.sexo.data if form.sexo.data else None,
            idade=form.idade.data,
            endereco=form.endereco.data.strip() if form.endereco.data else None,
            telefone=clean_numeric_input(form.telefone.data) if form.telefone.data else None,
            email=form.email.data.strip().lower() if form.email.data else None,
            foto_path=foto_filename,
            notas=form.notas.data.strip() if form.notas.data else None
        )
        
        try:
            db.session.add(paciente)
            db.session.commit()
            flash(f'Paciente {paciente.nome_completo} cadastrado com sucesso!', 'success')
            return redirect(url_for('perfil_paciente', id=paciente.id))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao cadastrar paciente. Tente novamente.', 'error')
            app.logger.error(f'Erro ao cadastrar paciente: {e}')
    
    return render_template('novo_paciente.html', form=form)

@app.route('/pesquisar-pacientes')
def pesquisar_pacientes():
    nome = request.args.get('nome', '').strip()
    cpf = request.args.get('cpf', '').strip()
    
    pacientes = []
    
    if nome or cpf:
        query = Paciente.query
        
        if nome:
            query = query.filter(Paciente.nome_completo.ilike(f'%{nome}%'))
        
        if cpf:
            cpf_clean = clean_numeric_input(cpf)
            query = query.filter(Paciente.cpf.like(f'%{cpf_clean}%'))
        
        pacientes = query.order_by(Paciente.nome_completo).all()
    
    return render_template('pesquisar_pacientes.html', pacientes=pacientes)

@app.route('/api/pesquisar-pacientes')
def api_pesquisar_pacientes():
    nome = request.args.get('nome', '').strip()
    cpf = request.args.get('cpf', '').strip()

    pacientes = []

    if nome or cpf:
        query = Paciente.query

        if nome:
            query = query.filter(Paciente.nome_completo.ilike(f'%{nome}%'))

        if cpf:
            cpf_clean = clean_numeric_input(cpf)
            query = query.filter(Paciente.cpf.like(f'%{cpf_clean}%'))

        pacientes = query.order_by(Paciente.nome_completo).all()

    # Convert pacientes to a list of dictionaries
    pacientes_list = [{
        'id': p.id,
        'nome_completo': p.nome_completo,
        'cpf': format_cpf(p.cpf),
        'telefone': format_phone(p.telefone),
        'email': p.email,
        'foto_path': p.foto_path,
    } for p in pacientes]

    return jsonify(pacientes_list)

@app.route('/paciente/<int:id>')
def perfil_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    tratamentos = Tratamento.query.filter_by(paciente_id=id).order_by(Tratamento.data_tratamento.desc()).all()
    
    return render_template('perfil_paciente.html', paciente=paciente, tratamentos=tratamentos)

@app.route('/tratamentos')
def tratamentos():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    tratamentos = Tratamento.query.order_by(Tratamento.data_tratamento.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('tratamentos.html', tratamentos=tratamentos)

@app.route('/arquivos')
def arquivos():
    # Get all patients for file organization
    pacientes = Paciente.query.order_by(Paciente.nome_completo).all()
    
    # Get uploaded files from uploads directory
    upload_dir = app.config['UPLOAD_FOLDER']
    arquivos_sistema = []
    
    if os.path.exists(upload_dir):
        for filename in os.listdir(upload_dir):
            if os.path.isfile(os.path.join(upload_dir, filename)):
                file_path = os.path.join(upload_dir, filename)
                file_stats = os.stat(file_path)
                
                # Find associated patient
                paciente_associado = None
                for p in pacientes:
                    if p.foto_path == filename:
                        paciente_associado = p
                        break
                
                arquivos_sistema.append({
                    'nome': filename,
                    'tamanho': file_stats.st_size,
                    'data_modificacao': datetime.fromtimestamp(file_stats.st_mtime),
                    'paciente': paciente_associado,
                    'tipo': 'foto' if paciente_associado else 'documento'
                })
    
    # Sort by modification date (newest first)
    arquivos_sistema.sort(key=lambda x: x['data_modificacao'], reverse=True)
    
    return render_template('arquivos.html', arquivos=arquivos_sistema, pacientes=pacientes)

@app.route('/upload-arquivo', methods=['POST'])
def upload_arquivo():
    if 'arquivo' not in request.files:
        flash('Nenhum arquivo selecionado.', 'error')
        return redirect(url_for('arquivos'))
    
    file = request.files['arquivo']
    paciente_id = request.form.get('paciente_id')
    descricao = request.form.get('descricao', '').strip()
    
    if file.filename == '':
        flash('Nenhum arquivo selecionado.', 'error')
        return redirect(url_for('arquivos'))
    
    # Validate file type (allow documents and images)
    allowed_extensions = {'pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png', 'gif'}
    if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
        flash('Tipo de arquivo não permitido. Use: PDF, DOC, DOCX, TXT, JPG, PNG, GIF.', 'error')
        return redirect(url_for('arquivos'))
    
    # Save file with descriptive name
    filename = secure_filename(file.filename)
    if paciente_id:
        paciente = Paciente.query.get(paciente_id)
        if paciente:
            # Create filename with patient name and description
            name_part = re.sub(r'[^a-zA-Z0-9]', '', paciente.nome_completo.replace(' ', '_'))
            desc_part = re.sub(r'[^a-zA-Z0-9]', '', descricao.replace(' ', '_')) if descricao else 'documento'
            ext = filename.rsplit('.', 1)[1].lower()
            filename = f"{name_part}_{desc_part}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
    
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        flash(f'Arquivo "{filename}" enviado com sucesso!', 'success')
    except Exception as e:
        flash('Erro ao fazer upload do arquivo.', 'error')
        app.logger.error(f'Erro no upload: {e}')
    
    return redirect(url_for('arquivos'))

@app.route('/download-arquivo/<filename>')
def download_arquivo(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except FileNotFoundError:
        flash('Arquivo não encontrado.', 'error')
        return redirect(url_for('arquivos'))

@app.route('/excluir-arquivo/<filename>', methods=['POST'])
def excluir_arquivo(filename):
    try:
        # Check if file is a patient photo
        paciente_com_foto = Paciente.query.filter_by(foto_path=filename).first()
        if paciente_com_foto:
            flash('Não é possível excluir a foto de um paciente. Exclua ou edite o paciente primeiro.', 'error')
            return redirect(url_for('arquivos'))
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            flash(f'Arquivo "{filename}" excluído com sucesso!', 'success')
        else:
            flash('Arquivo não encontrado.', 'error')
    except Exception as e:
        flash('Erro ao excluir arquivo.', 'error')
        app.logger.error(f'Erro ao excluir arquivo: {e}')
    
    return redirect(url_for('arquivos'))

@app.route('/novo-tratamento')
@app.route('/novo-tratamento/<int:paciente_id>')
def novo_tratamento(paciente_id=None):
    form = TratamentoForm()
    
    # Populate patient choices
    pacientes = Paciente.query.order_by(Paciente.nome_completo).all()
    form.paciente_id.choices = [(p.id, p.nome_completo) for p in pacientes]
    
    # Pre-select patient if provided
    if paciente_id:
        form.paciente_id.data = paciente_id
    
    paciente_selecionado = None
    if paciente_id:
        paciente_selecionado = Paciente.query.get_or_404(paciente_id)
    
    return render_template('novo_tratamento.html', form=form, paciente_selecionado=paciente_selecionado)

@app.route('/salvar-tratamento', methods=['POST'])
def salvar_tratamento():
    form = TratamentoForm()
    
    # Populate patient choices for validation
    pacientes = Paciente.query.order_by(Paciente.nome_completo).all()
    form.paciente_id.choices = [(p.id, p.nome_completo) for p in pacientes]
    
    #if form.validate_on_submit():
    paciente = Paciente.query.get_or_404(form.paciente_id.data)
    
    tratamento = Tratamento(
        paciente_id=paciente.id,
        nome_completo=paciente.nome_completo,
        queixa_principal=form.queixa_principal.data.strip() if form.queixa_principal.data else None,
        como=form.como.data.strip() if form.como.data else None,
        onde=form.onde.data.strip() if form.onde.data else None,
        exames_complementares=form.exames_complementares.data.strip() if form.exames_complementares.data else None,
        antecedentes=form.antecedentes.data.strip() if form.antecedentes.data else None,
        tratamentos_anteriores=form.tratamentos_anteriores.data.strip() if form.tratamentos_anteriores.data else None,
        qualidade_sono=form.qualidade_sono.data.strip() if form.qualidade_sono.data else None,
        movimentos=form.movimentos.data.strip() if form.movimentos.data else None,
        irradiacoes=form.irradiacoes.data.strip() if form.irradiacoes.data else None,
        conclusoes_tratamento=form.conclusoes_tratamento.data.strip() if form.conclusoes_tratamento.data else None,
        data_retorno=form.data_retorno.data,
        retorno=form.retorno.data.strip() if form.retorno.data else None
    )
    
    try:
        db.session.add(tratamento)
        db.session.commit()
        flash(f'Tratamento para {paciente.nome_completo} registrado com sucesso!', 'success')
        return redirect(url_for('perfil_paciente', id=paciente.id))
    except Exception as e:
        db.session.rollback()
        flash('Erro ao registrar tratamento. Tente novamente.', 'error')
        app.logger.error(f'Erro ao registrar tratamento: {e}')
    
    ## If form validation fails, redirect back with errors
    #for field, errors in form.errors.items():
    #    for error in errors:
    #        flash(f'{field}: {error}', 'error')
    
    return redirect(url_for('novo_tratamento', paciente_id=form.paciente_id.data))

@app.route('/editar-tratamento/<int:id>', methods=['GET', 'POST'])
def editar_tratamento(id):
    tratamento = Tratamento.query.get_or_404(id)
    form = TratamentoForm(obj=tratamento)
    
    # Populate patient choices
    pacientes = Paciente.query.order_by(Paciente.nome_completo).all()
    form.paciente_id.choices = [(p.id, p.nome_completo) for p in pacientes]
    
    if form.validate_on_submit():
        paciente = Paciente.query.get_or_404(form.paciente_id.data)
        
        # Update treatment data
        tratamento.paciente_id = paciente.id
        tratamento.nome_completo = paciente.nome_completo
        tratamento.queixa_principal = form.queixa_principal.data.strip() if form.queixa_principal.data else None
        tratamento.como = form.como.data.strip() if form.como.data else None
        tratamento.onde = form.onde.data.strip() if form.onde.data else None
        tratamento.exames_complementares = form.exames_complementares.data.strip() if form.exames_complementares.data else None
        tratamento.antecedentes = form.antecedentes.data.strip() if form.antecedentes.data else None
        tratamento.tratamentos_anteriores = form.tratamentos_anteriores.data.strip() if form.tratamentos_anteriores.data else None
        tratamento.qualidade_sono = form.qualidade_sono.data.strip() if form.qualidade_sono.data else None
        tratamento.movimentos = form.movimentos.data.strip() if form.movimentos.data else None
        tratamento.irradiacoes = form.irradiacoes.data.strip() if form.irradiacoes.data else None
        tratamento.conclusoes_tratamento = form.conclusoes_tratamento.data.strip() if form.conclusoes_tratamento.data else None
        tratamento.data_retorno = form.data_retorno.data
        tratamento.retorno = form.retorno.data.strip() if form.retorno.data else None
        tratamento.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash(f'Tratamento de {paciente.nome_completo} atualizado com sucesso!', 'success')
            return redirect(url_for('perfil_paciente', id=paciente.id))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao atualizar tratamento. Tente novamente.', 'error')
            app.logger.error(f'Erro ao atualizar tratamento: {e}')
    
    return render_template('editar_tratamento.html', form=form, tratamento=tratamento)

@app.route('/excluir-tratamento/<int:id>', methods=['POST'])
def excluir_tratamento(id):
    tratamento = Tratamento.query.get_or_404(id)
    paciente_id = tratamento.paciente_id
    
    try:
        db.session.delete(tratamento)
        db.session.commit()
        flash(f'Tratamento excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erro ao excluir tratamento. Tente novamente.', 'error')
        app.logger.error(f'Erro ao excluir tratamento: {e}')
    
    return redirect(url_for('perfil_paciente', id=paciente_id))

@app.route('/editar-paciente/<int:id>', methods=['GET', 'POST'])
def editar_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    form = PacienteForm(obj=paciente)
    
    if form.validate_on_submit():
        # Clean CPF
        cpf_clean = clean_numeric_input(form.cpf.data)
        
        # Check if CPF already exists (excluding current patient)
        #if cpf_clean:
        #    existing_patient = Paciente.query.filter(Paciente.cpf == cpf_clean, Paciente.id != id).first()
        #    if existing_patient:
        #        flash('Já existe outro paciente cadastrado com este CPF.', 'error')
        #        return render_template('editar_paciente.html', form=form, paciente=paciente)
        
        # Handle file upload
        if form.foto.data:
            foto_filename = save_uploaded_file(form.foto.data, app.config['UPLOAD_FOLDER'])
            if foto_filename:
                # Delete old photo if exists
                if paciente.foto_path:
                    old_photo_path = os.path.join(app.config['UPLOAD_FOLDER'], paciente.foto_path)
                    if os.path.exists(old_photo_path):
                        os.remove(old_photo_path)
                paciente.foto_path = foto_filename
            else:
                flash('Erro ao fazer upload da foto. Verifique o formato e tamanho do arquivo.', 'error')
                return render_template('editar_paciente.html', form=form, paciente=paciente)
        
        # Update patient data
        paciente.nome_completo = form.nome_completo.data.strip().title()
        paciente.cpf = cpf_clean
        paciente.profissao = form.profissao.data.strip() if form.profissao.data else None
        paciente.sexo = form.sexo.data if form.sexo.data else None
        paciente.idade = form.idade.data
        paciente.endereco = form.endereco.data.strip() if form.endereco.data else None
        paciente.telefone = clean_numeric_input(form.telefone.data) if form.telefone.data else None
        paciente.email = form.email.data.strip().lower() if form.email.data else None
        paciente.notas = form.notas.data.strip() if form.notas.data else None
        paciente.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash(f'Dados de {paciente.nome_completo} atualizados com sucesso!', 'success')
            return redirect(url_for('perfil_paciente', id=paciente.id))
        except Exception as e:
            db.session.rollback()
            flash('Erro ao atualizar dados do paciente. Tente novamente.', 'error')
            app.logger.error(f'Erro ao atualizar paciente: {e}')
    
    return render_template('editar_paciente.html', form=form, paciente=paciente)

@app.route('/excluir-paciente/<int:id>', methods=['POST'])
def excluir_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    
    try:
        # Delete photo if exists
        if paciente.foto_path:
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], paciente.foto_path)
            if os.path.exists(photo_path):
                os.remove(photo_path)
        
        # Delete patient (treatments will be deleted automatically due to cascade)
        db.session.delete(paciente)
        db.session.commit()
        flash(f'Paciente {paciente.nome_completo} excluído com sucesso!', 'success')
        return redirect(url_for('pesquisar_pacientes'))
    except Exception as e:
        db.session.rollback()
        flash('Erro ao excluir paciente. Tente novamente.', 'error')
        app.logger.error(f'Erro ao excluir paciente: {e}')
        return redirect(url_for('perfil_paciente', id=id))

# Template filters
@app.template_filter('format_cpf')
def format_cpf_filter(cpf):
    return format_cpf(cpf) if cpf else ''

@app.template_filter('format_phone')
def format_phone_filter(phone):
    return format_phone(phone) if phone else ''

# Template context processors
@app.context_processor
def inject_today():
    return {'today': date.today()}

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

# Create database tables
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True, host='0.0.0.0', port=5000)
