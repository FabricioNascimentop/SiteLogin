import os
from database import db, Usuario
from werkzeug.security import generate_password_hash, check_password_hash


contas_list = []
with open("contas.txt","r+") as contas:
    for conta in contas.readlines():
        conta =  conta.split()
        contas_list.append(conta)
c1 = 0
for item in contas_list:
    for i in item:
        c1 += 1
        if c1 <= 3:
            with open("contas.txt","w") as contas:
                contas.write,
        else:
            print('')
            c1 = 0

def validador(str,indice,local=False):
    """
#str - coisa a se validar
#indice: 0 = nome; 1 = email; 2 = senha
#local: retorna a linha em que a variável se encontra, default=False
retorna True quando o arquivo contas.txt possui o "str" na categoria "índice
"""

    with open("contas.txt","r") as contas:
        c = 0
        for palavras in contas.readlines():
            c += 1
            palavras = palavras.split()
            if str.lower() == palavras[indice].lower():
                return True, c
            if local:
                return True, c


def listador(indice):
    """
    Listas todos os elementos no índice pedido, o sendo:
    0 - nomes
    1 - emails
    2 - senhas
"""
    with open ('contas.txt','r') as contas:
        for coisas in contas.readlines():
            print(coisas.split()[indice])


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