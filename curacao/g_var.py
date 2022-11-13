# MONGO REMOTO
MONGO_URI = "mongodb+srv://legion:Legi0n$.2022@cluster0.spmg6.mongodb.net/?retryWrites=true&w=majority"
# MONGO LOCAL
MONGO_LOCAL = "mongodb://superuser:Viper.2013@192.168.9.66:27017/?authMechanism=DEFAULT&tls=false"
MONGO_LOCAL_MAC = "localhost"
# GLOBARL DATABASE  ( MONGO DB :   1 = REMOTE,  2 = LOCAL  )
mongo_db =  2
# GLOBARL PATH  ( 1 = MAC,  2 = WINDOW,  3 = HEROKU ))
global_variables = 1

if global_variables == 1:
    path_proxy='/Users/javier/GIT/fala/ripley/urls/proxies.txt' #   MAC


if global_variables ==  2:
    path_proxy=r'C:\\Git\\fala\\falabella\urls\\proxies.txt'  #   WINDOWS

    path_promart = "C:\\Git\\fala\\shopstar\\urls\\bs4_2.txt"   # WINDOWS

if global_variables == 3:
    path_wong = "wong//text//url.txt"  #H HEROKU
    path_shop= "shopstar/urls//bs4_2.txt"  # HEROKU PATH
    path_ripley='ripley/urls/proxies.txt' #   HEROKU
    path_ripley_links='ripley/urls/link.txt'  # HEROKU
    path_promart= "shopstar/urls//bs4_2.txt"  # HEROKU

if mongo_db == 1:
    mongo_db =  MONGO_URI

if mongo_db == 2:
   mongo_db =  MONGO_LOCAL

if mongo_db == 3:
    mongo_db =  MONGO_LOCAL_MAC

# lista de web urls
array_tec=[]
# lista de proxies
proxies=[]

f = open(path_proxy, "r")
x = f.readlines()
for i in x: 
    proxies.append(i.rstrip())

# f = open(path_ripley, "r")
# x = f.readlines()
# for i in x:
#      array_tec.append(i.rstrip())