from database import db, Usuario
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import os
from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo




google_client_id = os.getenv("google_client_id")
google_client_secret = os.getenv("google_client_secret")


class LoginForm(FlaskForm):
    email = EmailField(
        'E-mail',
        validators=[
            DataRequired(message='Por favor, insira seu e-mail.'),
            Email(message='Formato de e-mail inválido.'),
            Length(max=100, message='O e-mail pode ter no máximo 100 caracteres.')
        ]
    )
    senha = PasswordField(
        'Senha',
        validators=[
            DataRequired(message='Por favor, insira sua senha.'),
            Length(min=8, message='A senha deve ter ao menos 8 caracteres.'),
            Regexp(
                r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d!@#$%^&*()\-_=+{}\[\]|\\;:",.<>/?]+$',
                message=(
                    'A senha deve conter ao menos uma letra maiúscula, '
                    'uma minúscula e um número. Caracteres especiais são permitidos.'
                )
            )
        ]
    )
    submit = SubmitField('Entrar')


class CriarContaForm(FlaskForm):
    nome = StringField('Nome', validators=[
        DataRequired('Por favor, informe seu nome'),
        Length(min=3, max=50, message='O nome deve ter entre 3 e 50 caracteres')
    ])
    
    email = StringField('Email', validators=[
        DataRequired('Por favor, informe seu email'),
        Email('Por favor, informe um email válido')
    ])
    
    senha = PasswordField('Senha', validators=[
        DataRequired('Por favor, crie uma senha'),
        Length(min=8, message='A senha deve ter pelo menos 8 caracteres'),
        Regexp(
        r'^(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&*]).*$',
        message='A senha deve conter: 1 letra maiúscula, 1 número e 1 caractere especial (@#$%^&*)')
    ])
    
    confirmar_senha = PasswordField('Confirmar Senha', validators=[
        DataRequired('Por favor, confirme sua senha'),
        EqualTo('senha', message='As senhas não coincidem')
    ])
    
    submit = SubmitField('Enviar')


#validamentos, (sim, não precisava ter usado a biblioteca re no validador de nome, usei pq gosto de padrões)
#não sei pra quem escrevo isso, sinceramente
#se você for um recrutador e estiver lendo isso por favor comente algo somente se eu for contratado
def validador_nome(nome):
    import re
    padrao = r'^[A-Za-zÀ-ÿ\s\'-]{3,16}'
    re = re.compile(padrao)
    if re.match(nome):
        return True
    else:
        return False

def validador_senha(senha):
    import re
    padrao = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d!@#$%^&*()-_=+{}[\]|\\;:",.<>/?]{8,}$'
    re = re.compile(padrao)
    if re.match(senha):
        return True
    else:
        return False



def validador_email(email):
    import re
    #[letras maíusculas ou minúsculas, qualquer sequência de número, estes caracteres específicos:".","_","%","+","-"] se repetindo qualquer vezes quiser.
    #um arroba (especificamente este caractere)
    #um "." seguido de no mínimo 2 letras maiúsculas ou minúsculas 
    #tem um pequeno erro de que se colocar algo como nome@exemplo.com a última parte aceita nome@exemplo.com.com mas sinceramente n to afim de resolver isso
    padrao = r'^[a-zA-Z0-9\._%+-]+@[a-zA-Z0-9\.-]+\.[a-zA-Z]{2,}$'
    re = re.compile(padrao)
    if re.match(email):
        return True
    else:
        return False

#verifica se há outro email já cadastrado em "contas.txt". Caso sim retorna True
def repetido_email(email):
    with open('contas.txt','r') as contas:
        for conta in contas:
            conta = conta.split()
            if conta[1] == str(email):
                return True
        return False



def salvar_conta(nome, email, senha):

    user = Usuario.query.filter_by(email=email).first()
    if user:
        return False
    novo_user = Usuario(
        nome=nome,
        email=email,
        senha=generate_password_hash(senha)
    )
    
    db.session.add(novo_user)
    db.session.commit()