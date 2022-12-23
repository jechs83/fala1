text = open ("/Users/javier/GIT/fala/buscador/comandos.txt" ,"r")

line = text.readlines()
line = str(line)
line = line.replace("'","")[:-1][1:]
print(line)
  
