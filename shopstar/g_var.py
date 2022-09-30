# MONGO REMOTO
MONGO_URI = "mongodb+srv://legion:Legi0n$.2022@cluster0.spmg6.mongodb.net/?retryWrites=true&w=majority"
# MONGO LOCAL
MONGO_LOCAL = "mongodb://superuser:Viper.2013@192.168.9.66:27017/?authMechanism=DEFAULT&tls=false"

# GLOBARL DATABASE  (  REMOTE == 1 ,   LOCAL == 2  )
mongo_db =  2
# GLOBARL PATH  ( 1 = MAC    2 = WINDOW   3 = HEROKU  )
global_variables = 1


if global_variables == 1:
    path_proxy='/Users/javier/GIT/fala/ripley/urls/proxies.txt' #   MAC
    path_ripley_links='/Users/javier/GIT/fala/ripley/urls/link.txt'  # MAC
    path_ripley_links2='/Users/javier/GIT/fala/ripley/urls/link2.txt'  # MAC
    path_ripley_links3='/Users/javier/GIT/fala/ripley/urls/link3.txt'  # MAC
    path_ripley_links4='/Users/javier/GIT/fala/ripley/urls/link4.txt'  # MAC
    path_ripley_links5='/Users/javier/GIT/fala/ripley/urls/link5.txt'  # MAC
    path_ripley_links6='/Users/javier/GIT/fala/ripley/urls/link6.txt'  # MAC
    path_ripley_links7='/Users/javier/GIT/fala/ripley/urls/link7.txt'  # MAC
    path_ripley_links8='/Users/javier/GIT/fala/ripley/urls/link8.txt'  # MAC
    path_ripley_links9='/Users/javier/GIT/fala/ripley/urls/link9.txt'  # MAC
    path_ripley_links10='/Users/javier/GIT/fala/ripley/urls/link10.txt'  # MAC
    path_ripley_links11='/Users/javier/GIT/fala/ripley/urls/link11.txt'  # MAC
    path_ripley_links12='/Users/javier/GIT/fala/ripley/urls/link12.txt'  # MAC
    path_ripley_links12='/Users/javier/GIT/fala/ripley/urls/link13.txt'  # MAC
    path_ripley_links12='/Users/javier/GIT/fala/ripley/urls/link14.txt'  # MAC
    path_ripley_links12='/Users/javier/GIT/fala/ripley/urls/link15.txt'  # MAC
    path_ripley_links12='/Users/javier/GIT/fala/ripley/urls/link16.txt'  # MAC
    path_ripley_links12='/Users/javier/GIT/fala/ripley/urls/link17.txt'  # MAC
    path_ripley_links12='/Users/javier/GIT/fala/ripley/urls/link18.txt'  # MAC


    

if global_variables == 2:
    path_proxy=r'C:\\Git\\fala\\ripley\urls\\proxies.txt'  #   WINDOWS
    path_ripley_links=r"C:/Git/fala/ripley/urls/link.txt"  # WINDOWS
    path_ripley_links2=r"C:/Git/fala/ripley/urls/link2.txt"  # WINDOWS
    path_ripley_links3=r"C:/Git/fala/ripley/urls/link3.txt"  # WINDOWS
    path_ripley_links4=r"C:/Git/fala/ripley/urls/link4.txt"  # WINDOWS
    path_ripley_links5=r"C:/Git/fala/ripley/urls/link5.txt"  # WINDOWS
    path_ripley_links6=r"C:/Git/fala/ripley/urls/link6.txt"  # WINDOWS
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