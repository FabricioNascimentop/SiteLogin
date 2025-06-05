from flask import Flask, render_template, request, redirect, flash, session
import utilidades
from Emails import *
from database import db, DATABASE_URI, Usuario
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'Fabricio'

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

#página inicial
@app.route('/')
def inicio():
    return render_template('index.html')

#meramente a página de login
@app.route('/login')
def logar():
    return render_template('login.html')

#função e rota que autentica a entrada no site
#validação será melhorada considerando as contas que foram criadas no site
@app.route('/autenticar login',methods=['POST',])
def autenticar_login():
    email = request.form.get('Email')
    senhaa = request.form.get('SenhaLogin')


    user = Usuario.query.filter_by(email=email).first()

    if user:
        if check_password_hash(user.senha, senhaa):
            return render_template('site.html')
        else:
            flash('email ou senha incorreto')
            return redirect('/login')
    else:
        flash('não há usuários com este email')
        return redirect('/login')
    
    

#autenticar criação de conta 
@app.route('/autenticar conta',methods=['POST',])
def autenticar_conta():
    nome = request.form.get("Nomecriarconta")
    email = request.form.get("Emailcriarconta")
    senha = request.form.get("Senhacriaconta")

    user = Usuario.query.filter_by(email=email).first()

    erro = False

    if user:
        flash('este email já está cadastrado')
        erro = True
    else:
        if not utilidades.validador_nome(nome):
            flash('nome inválido', category="Nome")
            erro = True
        if not utilidades.validador_email(email):
            flash('email inválido', category="Email")
            erro = True
        if not utilidades.validador_senha(senha):
            flash('senha inválida', category="Senha")
            erro = True
        
        if utilidades.validador_nome(nome) and utilidades.validador_email(email) and utilidades.validador_senha(senha):
            flash('conta criada com sucesso')

        if erro:
            print('tem erro')
            return redirect('/criar conta')
        
        if not erro:
            try:
                novo_usuario = Usuario(nome=nome,email=email,senha=generate_password_hash(senha))
                db.session.add(novo_usuario)
                db.session.commit()
                flash('Conta criada com sucesso! Faça login para continuar.', 'success')

            except Exception as e:
                db.session.rollback()
                flash('Erro ao criar conta. Por favor, tente novamente.', 'Senha')
                return redirect('/criar conta')
                
        
            return render_template('site.html')
       


#retorna a página de criar conta
@app.route('/criar conta')
def criaconta():
    return render_template('cria_conta.html')

@app.route('/recuperar conta')
def recuperaconta():
    return render_template('recuperar_conta.html')

@app.route('/bgl de senha')
def senha_sla():
    return render_template('tela_senha.html')


@app.route('/verificar conta',methods=['POST',])
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
        return redirect('/bgl de senha')
    
    if not user:
        flash('Este email não existe no nosso sistema')
        return redirect('/recuperar conta')


@app.route('/validar codigo',methods=['POST',])
def validar_codigo():
    codigo_inserido = request.form.get('codigo_recusenha')
    if codigo_inserido == session["codigo"]:
        return redirect('/nova senha')
    else:
        flash('código errado, tente novamente')
        return redirect('/bgl de senha')

@app.route('/nova senha',methods=['POST','GET'])
def definir_nova_senha():
    if request.method == 'GET':
        return render_template('trocar_senha.html')
    else:
        nova_senha = request.form.get('nova_senha')
        

if __name__ == "__main__":
    app.run(debug=True)