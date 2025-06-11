# 🏥 Sistema de Gerenciamento de Pacientes de Osteopatia

## 📋 Instruções de Instalação e Execução

### 1. Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### 2. Instalação

1. **Clone ou baixe o projeto** para o diretório desejado

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Inicialize o banco de dados:**
```bash
python init_db.py
```

### 3. Executar o Sistema

```bash
python app.py
```

O sistema estará disponível em: **http://localhost:5000**

### 4. Funcionalidades Principais

#### 🏠 Página Inicial
- Dashboard com estatísticas
- Acesso rápido a todas as funcionalidades
- Atividades recentes

#### 👤 Gestão de Pacientes
- **Cadastrar Novo Paciente**: Formulário completo com todos os campos solicitados
- **Pesquisar Pacientes**: Busca por nome ou CPF
- **Perfil do Paciente**: Visualização completa dos dados e histórico
- **Editar Paciente**: Atualização de informações
- **Upload de Fotos**: Suporte a imagens JPG, PNG, GIF

#### 💊 Gestão de Tratamentos
- **Registrar Tratamento**: Formulário detalhado com todos os campos clínicos
- **Histórico de Tratamentos**: Visualização cronológica por paciente
- **Lista de Tratamentos**: Visão geral de todos os tratamentos

#### 🔍 Campos do Sistema

**Pacientes:**
- ID (auto-incrementado)
- Nome Completo
- Data de Registro (automática)
- Profissão
- Sexo
- Idade
- Endereço
- CPF (validação brasileira)
- Telefone
- Email
- Foto
- Notas livres

**Tratamentos:**
- ID do Tratamento (auto-incrementado)
- Nome Completo (preenchido automaticamente)
- Data do Tratamento (automática)
- Queixa Principal
- Como?
- Onde?
- Exames Complementares
- Antecedentes
- Tratamentos Anteriores
- Qualidade do Sono
- Movimentos
- Irradiações
- Conclusões e Tratamento
- Data de Retorno
- Retorno (observações)

### 5. Características Técnicas

#### 🔒 Segurança
- Validação de CPF brasileiro
- Proteção contra SQL Injection (SQLAlchemy ORM)
- Validação de uploads de arquivo
- Sanitização de dados de entrada
- Tokens CSRF para formulários

#### 📱 Interface
- Design responsivo (Bootstrap 5)
- Interface profissional e intuitiva
- Máscaras para CPF e telefone
- Validação em tempo real
- Feedback visual para ações

#### 💾 Armazenamento
- Banco de dados SQLite local
- Fotos armazenadas em pasta local
- Backup automático dos dados

### 6. Estrutura de Arquivos

```
PatientsManagerKilo/
├── app.py                 # Aplicação principal
├── config.py             # Configurações
├── init_db.py            # Inicialização do banco
├── requirements.txt      # Dependências
├── database/
│   ├── models.py        # Modelos do banco
│   └── database.db      # Banco SQLite
├── static/
│   ├── css/style.css    # Estilos
│   ├── js/main.js       # JavaScript
│   └── uploads/         # Fotos dos pacientes
├── templates/           # Templates HTML
└── utils/
    └── helpers.py       # Funções auxiliares
```

### 7. Funcionalidades Especiais

#### 📅 Agenda Google
- Botão que abre o Google Calendar em nova aba
- Integração simples conforme solicitado

#### 🔍 Pesquisa Avançada
- Busca por nome (parcial)
- Busca por CPF (parcial ou completo)
- Resultados em tempo real

#### 📊 Estatísticas
- Total de pacientes cadastrados
- Total de tratamentos realizados
- Atividades recentes

### 8. Validações Implementadas

- **CPF**: Validação completa do algoritmo brasileiro
- **Email**: Validação de formato
- **Telefone**: Máscara automática
- **Fotos**: Validação de tipo e tamanho
- **Campos obrigatórios**: Validação client-side e server-side

### 9. Backup e Segurança dos Dados

- Dados armazenados localmente em SQLite
- Fotos organizadas em pasta específica
- Relacionamentos com integridade referencial
- Exclusão em cascata (tratamentos são excluídos com o paciente)

### 10. Suporte e Manutenção

O sistema foi desenvolvido com:
- Código bem estruturado e comentado
- Arquitetura modular
- Fácil manutenção e extensão
- Logs de erro para debugging

### 🚀 Pronto para Uso!

O sistema está completo e pronto para uso profissional em consultórios de osteopatia, atendendo a todos os requisitos solicitados.

---

**Desenvolvido para profissionais de osteopatia - Interface profissional, segura e intuitiva.**