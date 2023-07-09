def validador(str,indice):
    """
#str - coisa a se validar
#indice: 0 = nome; 1 = email; 2 = senha
retorna True quando o arquivo contas.txt possui o "str" na categoria "índice
"""

    with open("contas.txt","r") as contas:
        for palavras in contas.readlines():
            palavras = palavras.split()
            if str.lower() == palavras[indice].lower():
                return True


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
    padrao = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d!@#$%^&*()-_=+{}[\]|\\;:",.<>/?]{8,}$'
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

#verifica se há outro email já cadastrado em "contas.txt"
def repetido_email(email):
    with open('contas.txt','r') as contas:
        for conta in contas:
            conta = conta.split()
            if conta[1] == str(email):
                return True
        return False



print(repetido_email('joaobosco@gmail.com'))