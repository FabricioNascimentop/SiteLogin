from flask import render_template, request, redirect, flash, Blueprint
from helper import LoginForm, CriarContaForm
from Emails import *
from database import db, Usuario
from werkzeug.security import generate_password_hash, check_password_hash

viewsBP = Blueprint('views', __name__)

#página inicial
@viewsBP.route('/')
def inicio():
    return render_template('index.html')

#meramente a página de login
@viewsBP.route('/login')
def logar():
    form = LoginForm()
    return render_template('login.html',form=form)



#retorna a página de criar conta
@viewsBP.route('/criar conta')
def criaconta():
    form = CriarContaForm()
    return render_template('cria_conta.html',form=form)

@viewsBP.route('/recuperar conta')
def recuperaconta():
    return render_template('recuperar_conta.html')

@viewsBP.route('/bgl de senha')
def senha_sla():
    email = request.args.get('email')
    return render_template('tela_senha.html', email=email)

@viewsBP.route('/nova senha')
def def_nova_senha():
    email = request.args.get('email')
    return render_template('trocar_senha.html',email=email)

@viewsBP.route('/site')
def site():
    return render_template('site.html')

