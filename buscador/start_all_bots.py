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
    subprocess.Popen([ "start", "cmd" , "/k",  "C:\Git\\fala\\buscador\\telegram_viper.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    subprocess.Popen([ "start", "cmd" , "/k", "C:\Git\\fala\\buscador\\telegram_excelsior.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    subprocess.Popen([ "start", "cmd" , "/k", "C:\Git\\fala\\buscador\\telegram_defiant.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    subprocess.Popen([ "start", "cmd" , "/k", "C:\Git\\fala\\buscador\\telegram_discovery.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    subprocess.Popen([ "start", "cmd" , "/k", "C:\Git\\fala\\buscador\\telegram_enterprise.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    subprocess.Popen([ "start", "cmd" , "/k",  "C:\Git\\fala\\buscador\\telegram_voyager.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    subprocess.Popen([ "start", "cmd" , "/k",  "C:\Git\\fala\\buscador\\telegram_tecno.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    subprocess.Popen([ "start", "cmd" , "/k",  "C:\Git\\fala\\buscador\\telegram_r2d2.py"], shell=True, executable="C:\windows\system32\cmd.exe")



    ## BOTS PARA LOS COMANDOS DE LAS NAVES
    #subprocess.Popen([ "start", "cmd" , "/k", "C:\Git\\fala\\buscador\\bot_voyager.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    #subprocess.Popen([ "start", "cmd" , "/k",  "C:\Git\\fala\\buscador\\bot_discovery.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    #subprocess.Popen([ "start", "cmd" , "/k", "C:\Git\\fala\\buscador\\bot_enterprise.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    subprocess.Popen([ "start", "cmd" , "/k", "C:\Git\\fala\\buscador\\bot_ds9.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    # subprocess.Popen([ "start", "cmd" , "/k", "C:\Git\\fala\\buscador\\bot_exelsior.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    subprocess.Popen([ "start", "cmd" , "/k",  "C:\Git\\fala\\buscador\\bot_viper.py"], shell=True, executable="C:\windows\system32\cmd.exe")


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



