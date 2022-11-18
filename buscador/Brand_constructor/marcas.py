# with open ("/Users/javier/GIT/fala/buscador/Brand_constructor/abarrotes.txt", "r" ) as f:
#     marcas = f.readlines()


# lista = []
# for i in marcas:
#     a= 're.compile("'
#     c ='",re.IGNORECASE)'
#     b= str(i.replace("\n",""))
#     t= a+b+c
#     lista.append(t)

# lista = str(lista)
# lista = lista.replace("'","").replace("[","").replace("]","")
# print(lista)
# final = open("/Users/javier/GIT/fala/buscador/Brand_constructor/marca_final.txt", "w")

# final.write(str(lista))

with open ("/Users/javier/GIT/fala/buscador/Brand_constructor/abarrotes.txt", "r" ) as f:
    marcas = f.readlines()

for i in marcas:

    