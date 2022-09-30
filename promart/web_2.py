array_tec=[]
path_mac='/Users/javier/GIT/fala/promart/urls/parte.txt'
path_window = "C:\\Git\\fala\\promart\\urls\\parte.txt"
heroku_path= "shopstar/urls//bs4_2.txt"
f = open(path_window, "r")
x = f.readlines()

for i in x:
   array_tec.append(i.rstrip()) 

