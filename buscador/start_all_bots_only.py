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
    
    #subprocess.Popen([ "start", "cmd" , "/k", "C:\Git\\fala\\buscador\\excelsior_telegram.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    #subprocess.Popen([ "start", "cmd" , "/k", "C:\Git\\fala\\buscador\\boyo_telegram.py"], shell=True, executable="C:\windows\system32\cmd.exe")

       
    #subprocess.Popen([ "start", "cmd" , "/k", "C:\Git\\fala\\buscador\\discovery_telegram.py"], shell=True, executable="C:\windows\system32\cmd.exe")
   
    #subprocess.Popen([ "start", "cmd" , "/k", "C:\Git\\fala\\buscador\\enterprise_telegram.py"], shell=True, executable="C:\windows\system32\cmd.exe")
  
    #subprocess.Popen([ "start", "cmd" , "/k",  "C:\Git\\fala\\buscador\\voyager_telegram.py"], shell=True, executable="C:\windows\system32\cmd.exe")


    ## BOTS PARA LOS COMANDOS DE LAS NAVES
    subprocess.Popen([ "start", "cmd" , "/k", "C:\git\\fala1\\buscador\\voyager.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    subprocess.Popen([ "start", "cmd" , "/k",  "C:\git\\fala1\\buscador\\discovery.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    subprocess.Popen([ "start", "cmd" , "/k", "C:\git\\fala1\\buscador\\enterprise.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    subprocess.Popen([ "start", "cmd" , "/k", "C:\git\\fala1\\buscador\\exelsior.py"], shell=True, executable="C:\windows\system32\cmd.exe")

    ## CADA 20 MINNUTOS SE REINICIA LOS BOTS 
    time.sleep(20*60) 

    ## MATGA TODOS LOS PROCESOS ANTES DE REINICIAR LA FUNCION START 
    subprocess.run(["taskkill", "/IM", "cmd.exe", "/F"])
    subprocess.run(["taskkill", "/IM", "py.exe", "/F"])
    time.sleep(10)

    start()
    


def stop():
    subprocess.run(["taskkill", "/IM", "py.exe", "/F"])
    time.sleep(10)
    
    
start()


