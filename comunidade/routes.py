from comunidade import app, database, bcrypt
from flask import render_template, redirect, url_for, flash, request
from comunidade.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from comunidade.models import Usuario, Post # Importa o modelo de usuário e post do banco de dados
from flask_login import login_user, logout_user, login_required, current_user # Biblioteca responsável por toda a parte de login/ logout e sessão do usuário no site
import secrets # Biblioteca responsável por gerar senhas aleatórias
import os # Biblioteca responsável por manipulação de arquivos e diretórios no servidor
from PIL import Image # Biblioteca Pillow responsável por manipulação de imagens (redimensionamento, etc.)
from datetime import datetime


# Início do site
@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc()) # Buscabdo todos os post do site, pelo Id e de forma decrescente
    return render_template('home.html', posts=posts) # Passa a lista de posts para a página inicial


# Página de Contatos
@app.route('/contatos')
def contatos():
    return render_template('contatos.html')


# Página de Usuários
@app.route('/usuarios')
@login_required # Só permite o acesso a essa página se o usuário estiver logado ao site
def usuarios():
    lista_usuarios = Usuario.query.all() # Busca todos os usuários cadastrados no banco de dados
    # Lista de usuários do site passada para a página
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


# Página de Login e Criação de Conta
@app.route('/login', methods=['GET', 'POST']) # Necesário infomrar os métodos para liberar a execução do POST dos formulários dessa página
def login():
    form_login = FormLogin() # Instancia do formulário de login a ser pasado para a página
    form_criarconta = FormCriarConta() # Instancia do formulário de criação de login a ser pasado para a página

    # Verifica se o formulario foi deviamente preenchido e validado e se o botão referente a este foi clicado
    # Verificação de qual botão foi clicado é necessário devido ao fato de haverem dois formulçários em uma mesma página
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        # LOGIN
        usuario = Usuario.query.filter_by(email=form_login.email.data).first() # Busca usuário pelo e-mail
        # Se o usuário existir e sua senha estiver certa
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data): # Passa a senha do banco e a que foi digitada para comparação
            # "Login_user" é a função do "Flask_login" que administra o login no site
            login_user(usuario, remember=form_login.lembrar.data) # Passamos o usuário encontrado no banco e o campo remember (se os dados devem ou não ser lembrados para o próximo login)
            # Utilizando o Flash passamos a mensagem e a categoria da mesma (categoria que será utilizada pelo código presente no base.html para apresentar e formatar o alerta)
            flash(f'Login feito com sucesso para o e-mail: {form_login.email.data}', 'alert-success') # categoria defnida pelo Bootstrap
            
            parametro_next = request.args.get('next') # Verifica se existe o parâmetro "next" na URL (caso o usuário tenha tentado acessar uma página restrita antes de logar)
            if parametro_next: # Se o parâmetro existir, redireciona para a página que o usuário queria acessar antes de logar
                return redirect(parametro_next) # Redireciona para a página que o usuário queria acessar antes de logar
            else:
                # Redireciona para a página de início utilizando o url_for para impedir a quebra de links
                return redirect(url_for('home'))
        else:
            flash(f'Falha no login. E-mail ou Senha incorretos', 'alert-danger') # categoria defnida pelo Bootstrap
        
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        # CRIAÇÂO DO USUÁRIO
        senha_crypt = bcrypt.generate_password_hash(form_criarconta.senha.data) # Criptografando a senha do usuário
        novo_usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_crypt)
        database.session.add(novo_usuario)
        database.session.commit()

        # Utilizando o Flash passamos a mensagem e a categoria da mesma (categoria que será utilizada pelo código presente no base.html para apresentar e formatar o alerta)
        flash(f'Conta criada com sucesso para o e-mail: {form_criarconta.email.data}', 'alert-success') # categoria defnida pelo Bootstrap
        # Redireciona para a página de início utilizando o url_for para impedir a quebra de links
        return redirect(url_for('home'))

    #Instancia dos formulários criados são passadas para a página
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


# Página de Logout
@app.route('/logout')
@login_required 
def logout():
    logout_user() # Função do Flask_login que faz o logout do usuário
    flash(f'Logout feito com sucesso', 'alert-success')
    # Redireciona para a página de início utilizando o url_for para impedir a quebra de links
    return redirect(url_for('home'))


# Página de Perfil do Usuário
@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil)) # Monta o link para acessar a foto de perfil do usuário logado com base no nome da imagem cadastrado no banco
    return render_template('perfil.html', foto_perfil=foto_perfil) # Passa o link da foto de perfil para a página



# Função responsável por salvar a imagem do usuário no servidor]
def salvar_imagem(imagem):
    # Adicionar um código aleatório ao nome da imagem para garantir que ela seja única no serivdor
    codigo = secrets.token_hex(8) # Gera um código hexadecimal aleatório de 16 caracteres (8 bytes)
    nome, extensao = os.path.splitext(imagem.filename) # Separa o nome do arquivo da extensão
    nome_final = nome + codigo + extensao # Monta o novo nome da imagem com o código gerado

    # Reduzir o tamanho da imagem
    tamanho_final = (200, 200) # Define o tamanho final da imagem
    imagem_reduzida = Image.open(imagem) # Abre a imagem utilizando a biblioteca Pillow
    imagem_reduzida.thumbnail(tamanho_final) # Reduz a imagem para o tamanho definido anteriormente
    
    # Salvar a imagem no servidor
    caminho_final = os.path.join(app.root_path, 'static/fotos_perfil', nome_final) # Monta o caminho completo para salvar a imagem no servidor
    imagem_reduzida.save(caminho_final) # Salva a imagem reduzida no servidor com o novo nome gerado

    return nome_final # Retorna o novo nome da imagem para ser salvo no banco de dados


# Função responsável por verificar no formulário de edição de perfil os cursos que forma marcados pelo usuário
def atualizar_cursos(formulario):
    lista_cursos = []
    # Varre o formuçário passado verificando os campos de curso que estão marcados
    for objeto in formulario:
        if 'curso_' in objeto.name: # Se for um dos campos de curso
            if objeto.data: # Se o campo estiver marcado
                lista_cursos.append(objeto.label.text) # Adiciona o nome do curso na lista de cursos

    # Se nenhum curso for marcado é preciso devolver o valor default 'Não Informado' para o campo cursos
    if len(lista_cursos) == 0:
        return 'Não Informado'
    else:
        return  ';'.join(lista_cursos) # Retorna a lista de cursos como uma string, separada por ';'


# Página de Edição de Perfil
@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form_perfil = FormEditarPerfil()
    if form_perfil.validate_on_submit(): # Se a validação do formulário for OK
        # Atualiza os dados do usuário logado com os dados do formulário
        current_user.username = form_perfil.username.data
        current_user.email = form_perfil.email.data
        # Se o usuário alterou a foto de perfil
        if form_perfil.foto_perfil.data:
            nome_imagem = salvar_imagem(form_perfil.foto_perfil.data) # Chama a função responsável por salvar a imagem no servidor e retorna o nome dela
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form_perfil) # Chama a função responsável por buscar no formulario os cursos que o usuário marcou
        database.session.commit() # Diferente do formulário de criação do usuário, aqui não há a necessidade da ação de adição do usuário (.add), pois o mesmo já existe em banco. Aqui seus dados são apenas atualizados
        flash('Perfil atualizado com sucesso', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET': # Se o método for GET, ou seja, o formulário estiver sendo carregado, preenche os campos com os dados do usuário logado
        form_perfil.username.data = current_user.username
        form_perfil.email.data = current_user.email

    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form_perfil=form_perfil)


# Página de Criação de Post
@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form_criarpost = FormCriarPost()
    if form_criarpost.validate_on_submit(): # Se o formulário for devidamente preenchido e validado
        novo_post = Post(titulo=form_criarpost.titulo.data, corpo=form_criarpost.corpo.data, autor=current_user) # Cria o novo post com os dados do formulário e o usuário logado como autor
        database.session.add(novo_post)
        database.session.commit()
        flash('Post criado com sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form_criarpost=form_criarpost)


# Página de Exibição/ Edição de Post
@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    # Busca-se o post pelo ID
    post = Post.query.get(post_id) # Aqui poder-se-ia utilizar o 'filter_by', mas como estamos lidando com o ID da tabela, utilizamos o 'get' que é mais performático
    if post is None: # Se o ID passado for de um post que não existe no banco
        flash('Post não encontrado', 'alert-danger') # Avisa ao usuário
        return redirect(url_for('home')) # Redireciona o mesmo para a home
    else:
        # Verifica se o usuário logado é o autor do post
        if current_user == post.autor:
            form = FormCriarPost()  # Sendo, cria-se uma instancia do formulário de criação do Post que será utilizada para edição do memso
            if request.method == 'GET': # Se a página estiver sendo lida (método GET), as inofmrações do post são carregadas no campo para edição
                form.titulo.data = post.titulo
                form.corpo.data = post.corpo
            elif form.validate_on_submit(): # Se o formulário for devidamente preenchido e validado
                post.titulo = form.titulo.data # Altera o titulo do post com o valor do formulário 
                post.corpo = form.corpo.data # Altera o corpo do post com o valor do formulário
                database.session.commit() # Salva as alterações no banco
                flash('Post editado com sucesso', 'alert-success')
                return redirect(url_for('home'))
        else:
            form = None # Caso contrário passa-se o formulário vazio
        
        # Chama a página de exibição do post, passando a referencia do mesmo e o formulário de criação para a edição do post, se for o caso
        return render_template('post.html', post=post, form_editarpost=form) 
    

# Página de Exclusão de Post
@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    # Busca-se o post pelo ID
    post = Post.query.get(post_id)
    if post is None:
        flash('Post não encontrado', 'alert-danger')
    else:
        # Verifica se o usuário logado é o autor do post
        if current_user == post.autor:
            database.session.delete(post) # Deleta o post do banco de dados
            database.session.commit()
            flash('Post excluído com sucesso', 'alert-warning')
        else:
            flash('Você não tem permissão para excluir esse post', 'alert-danger')

    return redirect(url_for('home'))
