#"head" do flask, importações iniciais, definição da variável "app", da secret kay
from flask import Flask, render_template, request, redirect, flash
from utilidades import validador
app = Flask(__name__)
app.secret_key = 'Fabricio'
#classe que unifica os dados do usuário, em outras palavras uma conta (futuramente serão guardados em um banco de dados)
class Usuario:
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

#página inicial (sem estilização ainda)
@app.route('/')
def inicio():
    return render_template('index.html')

#meramente a página de login (sem estilização)
@app.route('/login')
def logar():
    return render_template('login.html')

#função e rota que autentica a entrada no site
#validação será melhorada considerando as contas que foram criadas no site
@app.route('/autenticar login',methods=['POST',])
def autenticar_login():
    email = request.form['Email']
    senha = request.form['SenhaLogin']
    if validador(email,1) and validador(senha,2):
        return render_template('site.html')
    else:
        flash('DIGITASTE ALGO ERRADO')
        return redirect('/login')

#autenticar criação de conta 
#futuramente autenticará a validade de email
@app.route('/autenticar conta',methods=['POST',])
def autenticar_conta():
    nome = request.form.get("Nomecriarconta")
    email = request.form.get("Emailcriarconta")
    senha = request.form.get("Senhacriaconta")
    #guarda as contas criadas num arquivo txt sem segurança nenhuma
    #futuramente haverá uma validação de armazenar ou não de acordo com se já tem no arquivo
    with open ("contas.txt",'a') as contas:
        contas.write(f"\n{nome.replace(' ','-')} {email} {senha.replace(' ','-')}")
    return redirect('/')

#retorna a página de criar conta (sem estilização)
@app.route('/criar conta')
def criaconta():
    return render_template('cria_conta.html')



app.run(debug=True)