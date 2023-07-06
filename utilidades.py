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



def validador_nome(nome):
    if len(nome) > 3:
        return True

def validador_senha(senha):
    import re
    padrao = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    if padrao:
        return True



def validar_email(email):
    import re
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return True


print(validador_senha('a'))
