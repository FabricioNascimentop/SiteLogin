with open("contas.txt","r") as contas:
    for palavras in contas.readlines():
        palavras = palavras.split()
        print(palavras[1])
