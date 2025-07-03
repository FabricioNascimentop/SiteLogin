from flask import render_template, request, redirect, flash, Blueprint, session, url_for
from helper import validador_email, validador_nome, validador_senha, CriarContaForm
from Emails import *
from database import db, Usuario
from werkzeug.security import generate_password_hash, check_password_hash
from . import oauth
from flask_login import login_user, login_required, logout_user  # type: ignore # Para gerenciar logins


postsBP = Blueprint('auth', __name__)




#função e rota que autentica a entrada no site
@postsBP.route('/autenticar login',methods=['POST',])
def autenticar_login():
    email_input = request.form.get('email')
    senha_input = request.form.get('senha')
    user = Usuario.query.filter_by(email=email_input).first()
    if user:
        if check_password_hash(user.senha, senha_input):
            return render_template('site.html')
        else:
            flash('email ou senha incorreto')
            return redirect('/login')
    else:
        flash('não há usuários com este email')
        return redirect('/login')
    

#autenticar criação de conta 
@postsBP.route('/autenticar conta',methods=['POST',])
def autenticar_conta():
    form = CriarContaForm(request.form)
    
    if form.validate_on_submit():
        nome = form.nome.data
        email = form.email.data
        senha = form.senha.data
        
        # Verifica se o email já está cadastrado
        user = Usuario.query.filter_by(email=email).first()
        
        if user:
            flash('Este email já está cadastrado', 'email')
            return redirect(url_for('views.criaconta'))
        
        # Validações adicionais
        validacoes = True
        
        if not validador_nome(nome):
            flash('Nome inválido', 'nome')
            validacoes = False
        
        if not validador_email(email):
            flash('Email inválido', 'email')
            validacoes = False
        
        if not validador_senha(senha):
            flash('Senha inválida - deve ter pelo menos 8 caracteres', 'senha')
            validacoes = False
        
        if form.senha.data != form.confirmar_senha.data:
            flash('As senhas não coincidem', 'senha')
            validacoes = False
        
        if not validacoes:
            return redirect(url_for('views.criaconta'))
        
        # Tenta criar o novo usuário
        try:
            novo_usuario = Usuario(
                nome=nome,
                email=email,
                senha=generate_password_hash(senha)
            )
            
            db.session.add(novo_usuario)
            db.session.commit()
            
            flash('Conta criada com sucesso! Faça login para continuar.', 'success')
            return redirect(url_for('auth.logar'))
        
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao criar conta: {str(e)}")
            flash('Erro ao criar conta. Por favor, tente novamente.', 'error')
            return redirect(url_for('views.criaconta'))
    
    # Se o formulário não for válido, coletar erros e redirecionar
    for field, errors in form.errors.items():
        for error in errors:
            print(field,error)
            flash(error, 'error')
    
    return redirect(url_for('views.criaconta'))          
        
  


@postsBP.route('/validar codigo',methods=['POST',])
def validar_codigo():
    codigo_inserido = request.form.get('codigo_recusenha')
    email = request.form.get('email')
    if codigo_inserido == session["codigo"]:
        return redirect(f'/nova senha?email={email}')
    else:
        flash('código errado, tente novamente')
        return redirect('/bgl de senha')



@postsBP.route('/nova senha',methods=['POST'])
def definir_nova_senha():
        nova_senha = request.form.get('nova_senha')
        email = request.form.get('email')
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario:
            usuario.set_password(nova_senha)
            db.session.commit()
        return redirect('/site')

  
@postsBP.route('/recuperar conta',methods=['POST'])
def veloconta():

    email = request.form.get('emailrecuperarconta')
    user = Usuario.query.filter_by(email=email).first()
    
    if email == '':
        flash('por favor digite um email válido')
        return redirect('/recuperar conta')
    
    if user:
        destinatario = email
        codigo = gera_codigo()
        session["codigo"] = codigo
        enviar_email('Restauração de senha',f'{retorna_html(codigo)}','fabnasctest@gmail.com',destinatario)
        return redirect(f'/bgl de senha?email={email}')
    
    if not user:
        flash('Este email não existe no nosso sistema')
        return redirect('/recuperar conta')

@postsBP.route('/login/facebook')
def facebook():
    """Começa o login pelo Facebook"""
    redirect_uri = url_for('auth.facebook_auth', _external=True)  
    return oauth.facebook.authorize_redirect(redirect_uri) 

@postsBP.route('/facebook/callback')
def facebook_auth():
    """Volta do Facebook com a resposta"""
    try:
        # Pega o token de acesso do Facebook
        token = oauth.facebook.authorize_access_token()
        # Pega informações do usuário
        resp = oauth.facebook.get('https://graph.facebook.com/me?fields=id,name,email')
        profile = resp.json()
        
        if 'error' in profile:
            return redirect('/login_failed')  # Se deu erro
        else:
            # Pega informações do perfil
            user_id = profile.get('id')
            user_name = profile.get('name', 'Usuário')
            user_email = profile.get('email', '')

            # Verifica se o usuário já existe
            usuario = Usuario.query.filter_by(email=user_email).first()
            if usuario:
                login_user(usuario)  # Faz login
                return redirect(f'/?name={user_name}&email={user_email}&id={user_id}')
            else:
                # Cria novo usuário
                usuario = Usuario(nome=user_name, email=user_email)
                db.session.add(usuario)
                db.session.commit()
                return redirect('/')

    except Exception as e:
        print("Erro:", str(e))
        return redirect('/login_failed')