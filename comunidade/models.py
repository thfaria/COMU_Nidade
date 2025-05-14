from comunidade import database, login_manager
from datetime import datetime
from flask_login import UserMixin # Biblioteca responsável por administrar o acesso do usuário ao site a partir do login


# Função que retorna um usuário com base em seu ID infromado.
# Necessária para o funcionamento do login_manager
@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario)) # POr se tratar de uma busca pela chave primária da tabela utilizamos o ".GET" ao invés de algum filterby



# Cada tabela no seu banco de dados é criada a partir de uma classe que é uma sub-classe da classe "Model" do SQLAlchemy

# TABELA DE USUÁRIOS (Atributos)
class Usuario(database.Model, UserMixin): #Atribuião do UserMixin indicando ao flask_login que o controle de acesso ao site é feito com essa tabela
    id = database.Column(database.Integer, primary_key=True) # 'primary_key=True' define esse como a cjhave primária da tabela
    username = database.Column(database.String, nullable=False) # 'nullable=False' define que o campo não pode ser nulo
    email = database.Column(database.String, nullable=False, unique=True) # 'unique=True' define que o conteudo do campo deve ser único no banco
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg') # 'default' define um valor default para esse campo
    post = database.relationship('Post', backref='autor', lazy=True) # relationship é uma coluna de relacionamento 1/N entre essa tabela e a outra
    cursos = database.Column(database.String, nullable=False, default='Não Informado')

    # Método que retorna o número de posts do usuário
    def contar_posts(self):
        return len(self.post) # Retorna o número de posts do usuário. O "self.post" é a relação 1/N entre as tabelas, ou seja, todos os posts do usuário
    

# TABELA DE POSTS (Atributos)
class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False) # Chave estrangeira para a tabela de Usuários. Precisa ter o nome da classe e do atributo (TUDO EM MINUSCULO)