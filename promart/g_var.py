# MONGO REMOTO
MONGO_URI = "mongodb+srv://legion:Legi0n$.2022@cluster0.spmg6.mongodb.net/?retryWrites=true&w=majority"
# MONGO LOCAL
MONGO_LOCAL = "mongodb://superuser:Viper.2013@192.168.9.66:27017/?authMechanism=DEFAULT&tls=false"

# GLOBARL DATABASE  ( MONGO DB :   1 = REMOTE,  2 = LOCAL  )
mongo_db =  2
# GLOBARL PATH  ( 1 = MAC,  2 = WINDOW,  3 = HEROKU ))
global_variables = 2

if global_variables == 1:
  
    path_promart='/Users/javier/GIT/fala/promart/urls/parte.txt'  # MAC
    path_proxy = '/Users/javier/GIT/fala/promart/urls/proxy.txt'

if global_variables == 2:

    path_promart = "C:\\Git\\fala\\promart\\urls\\bs4_2.txt"   # WINDOWS
    path_proxy = "C:\\Git\\fala\\promart\\urls\\proxy.txt" 

if global_variables == 3:

    path_promart= "promart/urls//bs4_2.txt"  # HEROKU
    path_proxy = 'promart/urls/proxy.txt'

if mongo_db == 1:
    mongo_db =  MONGO_URI

if mongo_db == 2:
   mongo_db =  MONGO_LOCAL

# lista de proxies
proxies=[]

f = open(path_proxy, "r")
x = f.readlines()
for i in x: 
    proxies.append(i.rstrip())

