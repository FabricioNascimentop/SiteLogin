#retorna o html que se envia ao email, como é um trecho imenso feio, horroroso, mequetrefe, deixo ele escondido aqui
def retorna_html(codigo):
    style = """body{
    }
    div{
        background-color: rgb(0,0,0,0.5);
        padding: 25px;
        font-size: 44px;
        text-align: center;
    }
    h1{
    font-size:24px;
    text-align: center;
    color: pink;
    }
    p{
    font-size:12px;
    }
    p#codigo{
        font-size:36px;
    }"""

    
    texto = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HTML aaaa</title>
</head>
<body>
    <h1 id="titulo">Olá, aqui está seu código de verificação</h1>
    <div>
        <p id="codigo">{codigo}</p>
    </div>
    <p>codigo, html e projeto feito por fabricio_nascimento</p>
    <a href="https://github.com/FabricioNascimentop" target="_blank">github.com/FabricioNascimentop</a>
</body>
<style>
{style}
</style>"""
    return texto


#usa a biblioteca smtplib pra enviar um email, um facilitador que basta colocar os parâmetros certos com uma conta preparada para tal
def enviar_email(assunto, texto, remetente, destinatário):
    import smtplib
    import email.message  
    corpo_email = texto
    msg = email.message.Message()
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = destinatário
    password = 'ccennanwwicisxik'
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)
    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    
#gera o código único a ser usado, código nada elegante porém exageradamente funcional, uma solução simples, nada elegante que me serve feito uma luva
def gera_codigo():
    from random import randint, choice    
    lista = []
    for c in range(0,9):
        numero = randint(0,9)
        letra = choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
        n = randint(0,10)
        if n <= 5:
            lista.append(numero)
        else:
            lista.append(letra)
    codigo = str(lista[0])+str(lista[1])+str(lista[2])+str(lista[3])+str(lista[4])+str(lista[5])+str(lista[6])+str(lista[7])+str(lista[8])
    return codigo