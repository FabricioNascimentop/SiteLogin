i = 0
for c in range(0,20):
    with open("contas.txt", "r") as contas:
        print(contas.readlines()[i])
    i += 4


