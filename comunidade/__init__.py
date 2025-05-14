from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

# Configurações de APP
app = Flask(__name__)

app.config['SECRET_KEY'] = '1e91b3613e9dc38444e4a83a7f1c626b' # Chave de segurança dos formulários 

# Definição do local do Banco de dados 
if os.getenv('DATABASE_URL'): # Caso a variável de ambiente DATABASE_URL esteja definida
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') # O banco de dados será o que estiver definido nela
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # ConfiguraçãoCaso contrário pega um caminho local

# Associação do Banco de Dados ao site
database = SQLAlchemy(app)

bcrypt = Bcrypt(app) # Criptografia para utilização com a senha dos usuários
login_manager = LoginManager(app) # Administração da parte de login do 
login_manager.login_view = 'login' # Indica para onde o usuário deve ser redirecionado caso tente acessar alguma página exclusive para quem esta logado sem estar
login_manager.login_message = 'Você precisa estar logado para acessar essa página' # Mensagem que será apresentada para o usuário caso ele não esteja logado e tente acessar uma página exclusiva
login_manager.login_message_category = 'alert-info' # Categoria da mensagem que será apresentada para o usuário


# Após configuração do app e definição do banco, cha-se o arquivo com a definição dos Routes que de fato vão criar o site
from comunidade import routes
