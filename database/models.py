from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Paciente(db.Model):
    __tablename__ = 'pacientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(200), nullable=False)
    data_registro = db.Column(db.Date, nullable=False, default=datetime.utcnow().date())
    profissao = db.Column(db.String(100))
    sexo = db.Column(db.String(20))
    idade = db.Column(db.Integer)
    endereco = db.Column(db.Text)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    foto_path = db.Column(db.String(200))
    notas = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamento com tratamentos
    tratamentos = db.relationship('Tratamento', backref='paciente', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Paciente {self.nome_completo}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome_completo': self.nome_completo,
            'data_registro': self.data_registro.strftime('%d/%m/%Y') if self.data_registro else None,
            'profissao': self.profissao,
            'sexo': self.sexo,
            'idade': self.idade,
            'endereco': self.endereco,
            'cpf': self.cpf,
            'telefone': self.telefone,
            'email': self.email,
            'foto_path': self.foto_path,
            'notas': self.notas,
            'created_at': self.created_at.strftime('%d/%m/%Y %H:%M') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%d/%m/%Y %H:%M') if self.updated_at else None
        }

class Tratamento(db.Model):
    __tablename__ = 'tratamentos'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    nome_completo = db.Column(db.String(200), nullable=False)
    data_tratamento = db.Column(db.Date, nullable=False, default=datetime.utcnow().date())
    queixa_principal = db.Column(db.Text)
    como = db.Column(db.Text)
    onde = db.Column(db.Text)
    exames_complementares = db.Column(db.Text)
    antecedentes = db.Column(db.Text)
    tratamentos_anteriores = db.Column(db.Text)
    qualidade_sono = db.Column(db.String(100))
    movimentos = db.Column(db.Text)
    irradiacoes = db.Column(db.Text)
    conclusoes_tratamento = db.Column(db.Text)
    data_retorno = db.Column(db.Date)
    retorno = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Tratamento {self.id} - {self.nome_completo}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'paciente_id': self.paciente_id,
            'nome_completo': self.nome_completo,
            'data_tratamento': self.data_tratamento.strftime('%d/%m/%Y') if self.data_tratamento else None,
            'queixa_principal': self.queixa_principal,
            'como': self.como,
            'onde': self.onde,
            'exames_complementares': self.exames_complementares,
            'antecedentes': self.antecedentes,
            'tratamentos_anteriores': self.tratamentos_anteriores,
            'qualidade_sono': self.qualidade_sono,
            'movimentos': self.movimentos,
            'irradiacoes': self.irradiacoes,
            'conclusoes_tratamento': self.conclusoes_tratamento,
            'data_retorno': self.data_retorno.strftime('%d/%m/%Y') if self.data_retorno else None,
            'retorno': self.retorno,
            'created_at': self.created_at.strftime('%d/%m/%Y %H:%M') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%d/%m/%Y %H:%M') if self.updated_at else None
        }