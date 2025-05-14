from flask_wtf import FlaskForm # Biblioteca de formulários
from flask_wtf.file import FileField, FileAllowed # Biblioteca de upload de arquivos
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField # Biblioteca de tipos de campos e botões
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError # Biblioteca de validadores de campos
from comunidade.models import Usuario
from flask_login import current_user # Biblioteca responsável por manter os dados do usuário logado no site


# Criação da classe do formulário de Criação de Conta com seus campos e botões
class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação de Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    # Função que verifica se o e-mail já existe no banco de dados
    # O nome "validate_" faz com que essa função seja chamada automaticamente pelo método "validate_on_submit()" da biblioteca "wtforms.validators"
    def validate_email(self, email):
        email_existente = Usuario.query.filter_by(email=email.data).first() # Busca se existe algum usuário cadastrado com o e-mail infomrado
        if email_existente: # Se algo for encontrado essa variável estará preenchida
            raise ValidationError('E-mail já cadastrado. Utilize outro e-mail ou faça Login para proseguir')


# Criação da classe do formulário de Login com seus campos e botões
class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar = BooleanField('Lembrar de mim')
    botao_submit_login = SubmitField('Login')


# Criação da classe do formulário de Edição do Perfil do Usuário
class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Foto de Perfil', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Apenas arquivos jpg, jpeg e png são aceitos')]) # Campo do tipo carregador de arquivo. Informa no validador os formatos de arquivo esperados e a mensagem a ser apresentada em caso de erro
    curso_a = BooleanField('Curso A')
    curso_b = BooleanField('Curso B')
    curso_c = BooleanField('Curso C')
    curso_d = BooleanField('Curso D')
    curso_e = BooleanField('Curso E')
    botao_submit_editarperfil = SubmitField('Confirmar Edição')

    # Função que verifica se o usuário alterou o e-mail dele e, nesse caso, verifica se o novo e-mail informado já existe ou não na base
    # Lembrando que obrigatoriamente a função precisa começar com "validate_" para ser chamada automaticamente pelo método "validate_on_submit()"
    def validate_email(self, email):
        # Verifica se o e-mail foi alterado
        if current_user.email != email.data:
            email_existente = Usuario.query.filter_by(email=email.data).first() # Busca se existe algum usuário cadastrado com o e-mail infomrado
            if email_existente: # Se algo for encontrado essa variável estará preenchida
                raise ValidationError('Esse e-mail já esta cadastrado para outro usuário, por favor informe um e-mail diferente')
            

# Criação da classe do formulário de Criação de Posts
class FormCriarPost(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(2, 140)]) # Obrigatório e com tamanho limitado de 2 a 140 caracteres
    corpo = TextAreaField('Escreva seu Post aqui', validators=[DataRequired()]) # Campo do tipo TextArea (maior) e obrigatório
    botao_submit_post = SubmitField('Postar')    
