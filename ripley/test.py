import sys
array_tec=[]
arg_ = sys.argv[1]
num = sys.argv[1]
arg_ = "/Users/javier/GIT/fala/ripley/urls/test/ripley"+str(num)+".txt"

f = open(arg_, "r")
x = f.readlines()
for i in x:
    array_tec.append(i.split()) 



print(array_tec)
# lista = []
# inicio = None
# for i,v  in enumerate  (array_tec):
#     if i ==0:

#     for i in range (15):
#         lista.append(v+str(i+1))