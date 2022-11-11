with open ("//Users//javier//GIT//fala//ripley//urls//test//ripley0.txt", "r") as f:
   x =  f.readlines()
print(len(x))

for idx, v in enumerate (x):

    x = (idx+500)-idx
    if idx == x:
        print(v)

    #  list.append()
    # if idx == 499:
    #     print(v)
    # # print(i+501)
    # # print(i.replace("\n",""))

