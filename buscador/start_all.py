import time
import subprocess
from pymongo import MongoClient
from decouple import config

client = MongoClient(config("MONGO_DB"))


## SOLO FUNCIONA  EN WINDOWS 
def start():

    db1 = client["scrap"]
    collection1 = db1["auto"]
    ex = collection1.find_one({"_id":"ex"})
    en = collection1.find_one({"_id":"en"})
    vo = collection1.find_one({"_id":"vo"})
    di = collection1.find_one({"_id":"di"})
    
    ##  BUSCADORES DE BASE DE DATOS  - ENVIA A TELGRAM LAS OFERTAS 
    bot1 = "telegram_ripley70-100.py"
    bot2= "telegram_saga70-100.py"
    bot3= "telegram_curacao70-100.py"
    bot4= "telegram_oh70-100.py"
    bot5= "telegram_promart70-100.py"
    bot6= "telegram_plaza70-100.py"
    bot7= "telegram_tailoy70-100.py"
    bot8= "telegram_platano70-100.py"
    
    lista = [bot1,bot2,bot3,bot5,bot6,bot7,bot8]

    for i in lista:
        subprocess.Popen([ "start", "cmd" , "/k", "C:\Git\\fala\\buscador\\{i}"], shell=True, executable="C:\windows\system32\cmd.exe")




    # subprocess.Popen([ "start", "cmd" , "/k", "C:\Git\\fala\\buscador\\{bot1}"], shell=True, executable="C:\windows\system32\cmd.exe")

    # subprocess.Popen([ "start", "cmd" , "/k", "C:\Git\\fala\\buscador\\{bot2}"], shell=True, executable="C:\windows\system32\cmd.exe")

    # subprocess.Popen([ "start", "cmd" , "/k",  "C:\Git\\fala\\buscador\\{bot3}], shell=True, executable="C:\windows\system32\cmd.exe")

    # subprocess.Popen([ "start", "cmd" , "/k",  "C:\Git\\fala\\buscador\\telegram_oh70-100.py"], shell=True, executable="C:\windows\system32\cmd.exe")

    # subprocess.Popen([ "start", "cmd" , "/k",  "C:\Git\\fala\\buscador\\telegram_promart70-100.py"], shell=True, executable="C:\windows\system32\cmd.exe")

    # subprocess.Popen([ "start", "cmd" , "/k",  "C:\Git\\fala\\buscador\\telegram_plaza70-100.py"], shell=True, executable="C:\windows\system32\cmd.exe")


    # subprocess.Popen([ "start", "cmd" , "/k",  "C:\Git\\fala\\buscador\\telegram_tailoy70-100.py"], shell=True, executable="C:\windows\system32\cmd.exe")

    # subprocess.Popen([ "start", "cmd" , "/k",  "C:\Git\\fala\\buscador\\telegram_platano70-100.py"], shell=True, executable="C:\windows\system32\cmd.exe")

    time.sleep(60) 

    ## MATGA TODOS LOS PROCESOS ANTES DE REINICIAR LA FUNCION START 
    subprocess.run(["taskkill", "/IM", "cmd.exe", "/F"])
    subprocess.run(["taskkill", "/IM", "py.exe", "/F"])
    time.sleep(5)

    start()
    


def stop():
    subprocess.run(["taskkill", "/IM", "py.exe", "/F"])
    time.sleep(10)
    
     
try:
    start()
except:
    start()



