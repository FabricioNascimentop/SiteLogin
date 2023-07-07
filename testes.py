with open('contas.txt','r') as contas:
    for conta in contas:
        conta = conta.split()
        print(conta[1])