with open ('contas.txt','r') as contas:
    for coisas in contas.readlines():
        print(coisas.split()[2])