#"head" do flask, importações iniciais, definição da variável "app", da secret kay
from flask import Flask, render_template, request, redirect, flash, session
import utilidades
from Emails import *
app = Flask(__name__)
app.secret_key = 'Fabricio'
app.config["SESSION_PERMANENT"] = False


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
    senha = request.form.get('SenhaLogin')
    senha = str(senha).replace(' ','-')
    if utilidades.validador(email,1) and utilidades.validador(senha,2):
        return render_template('site.html')
    else:
        flash('Email ou senha incorretos')
        return redirect('/login')


#autenticar criação de conta 
@app.route('/autenticar conta',methods=['POST',])
def autenticar_conta():
    val = False
    nome = request.form.get("Nomecriarconta")
    email = request.form.get("Emailcriarconta")
    senha = request.form.get("Senhacriaconta")

    if utilidades.validador_senha(senha) == False:
        flash(' a senha não é válida','Senha')
    elif utilidades.validador_email(email) == False:
        flash(' o email não é válido','Email')
    elif utilidades.validador_nome(nome) == False:
        flash('este nome não é válido','Nome')
    elif utilidades.repetido_email(email) == True:
        flash('este email  já está cadastrado','Email')
    else:
        with open ("contas.txt",'a') as contas:
            contas.write(f"\n{nome.replace(' ','-')} {email} {senha.replace(' ','-')}")
        return render_template('site.html')
       


#retorna a página de criar conta (sem estilização)
@app.route('/criar conta')
def criaconta():
    return render_template('cria_conta.html')

@app.route('/recuperar conta')
def recuperaconta():
    return render_template('recuperar_conta.html')

@app.route('/bgl de senha')
def senha_sla():
    return render_template('tela_senha.html')


@app.route('/vel conta',methods=['POST',])
def veloconta():
    email = request.form.get('emailrecuperarconta')
    print(email)
    if email == '':
        flash('por favor digite um email válido')
        return redirect('/recuperar conta')
    else:
        if utilidades.repetido_email(email) == True:
            destinatario = email
            codigo = gera_codigo()
            session["codigo"] = codigo
            enviar_email('Restauração de senha',f'{retorna_html(codigo)}','fabnasctest@gmail.com',destinatario)
            return redirect('/bgl de senha')
        else:
            flash('Este email não existe no nosso sistema')
            return redirect('/recuperar conta')


@app.route('/validar codigo',methods=['POST',])
def validar_codigo():
    codigo_inserido = request.form.get('codigo_recusenha')
    if codigo_inserido == session["codigo"]:
        return redirect('/nova senha')
    else:
        return redirect('/bgl de senha')

@app.route('/nova senha',methods=['POST','GET'])
def definir_nova_senha():
    if request.method == 'GET':
        return render_template('trocar_senha.html')
    else:
        nova_senha = request.form.get('nova_senha')
        














app.run(debug=True)