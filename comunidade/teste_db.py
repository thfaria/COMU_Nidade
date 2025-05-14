from comunidade.models import Usuario, Post
from comunidade import app, database


# Todo o comando de banco de dados precisa ser executado dentro de um contexto de aplicação 
with app.app_context():

    # CRIAÇÃO DO BANCO DE DADOS 
    # Executado apenas no momento da criação do banco de aparece na pasta 'instance' na raiz do site
    database.create_all()


    # INSERT DE DADOS EM UMA TABELA
    # Passamos para a classe que esta sendo criada as informações obrigatórias
    #usuario = Usuario(username='Thiago', email='thfaria@gmail.con', senha='Jubis1327')
    #usuario2 = Usuario(username='Juliana', email='jubis@gmail.con', senha='ChouChou1234')

    # Adicionamos as infromações à sessão do banco
    #database.session.add(usuario)
    #database.session.add(usuario2)

    # Realizamos o commit. 
    #database.session.commit()

    #post1 = Post(titulo='Meu primeiro post', corpo='Esse é o meu primeiro post', id_usuario=1)
    #database.session.add(post1)
    #database.session.commit()


    # SELECT EM UMA TABELA
    #meus_usuarios = Usuario.query.all() # Traz a tabela toda em forma de lista
    #primeiro_usuário = Usuario.query.first() # Traz o primeiro registro da tabela
    #usuario_x = Usuario.query.filter_by(username='Juliana').first() # Select com Where


    #print(usuario_x)
    #print(meus_usuarios)
    #print(primeiro_usuário.username)
    #print(primeiro_usuário.post[0].titulo)


    # APAGANDO O BANCO
    #database.drop_all()
    # E recriando ele vazio
    #database.create_all()