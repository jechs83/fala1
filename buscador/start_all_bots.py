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
    subprocess.Popen([ "start", "cmd" , "/k",  "C:\Git\\fala\\buscador\\telegram_borg_curacao.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    subprocess.Popen([ "start", "cmd" , "/k", "C:\Git\\fala\\buscador\\telegram_borg_ripley.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    subprocess.Popen([ "start", "cmd" , "/k",  "C:\Git\\fala\\buscador\\telegram_borg_saga.py"], shell=True, executable="C:\windows\system32\cmd.exe")

    subprocess.Popen([ "start", "cmd" , "/k",  "C:\Git\\fala\\buscador\\telegram_ripley60-70.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    subprocess.Popen([ "start", "cmd" , "/k", "C:\Git\\fala\\buscador\\telegram_ripley70-100.py"], shell=True, executable="C:\windows\system32\cmd.exe")

    subprocess.Popen([ "start", "cmd" , "/k", "C:\Git\\fala\\buscador\\telegram_saga60-70.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    subprocess.Popen([ "start", "cmd" , "/k", "C:\Git\\fala\\buscador\\telegram_saga70-100.py"], shell=True, executable="C:\windows\system32\cmd.exe")

    subprocess.Popen([ "start", "cmd" , "/k", "C:\Git\\fala\\buscador\\telegram_curacao60-70.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    subprocess.Popen([ "start", "cmd" , "/k",  "C:\Git\\fala\\buscador\\telegram_curacao70-100.py"], shell=True, executable="C:\windows\system32\cmd.exe")

    subprocess.Popen([ "start", "cmd" , "/k",  "C:\Git\\fala\\buscador\\telegram_oh60-70.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    subprocess.Popen([ "start", "cmd" , "/k",  "C:\Git\\fala\\buscador\\telegram_oh70-100.py"], shell=True, executable="C:\windows\system32\cmd.exe")

    subprocess.Popen([ "start", "cmd" , "/k",  "C:\Git\\fala\\buscador\\telegram_promart70-100.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    subprocess.Popen([ "start", "cmd" , "/k",  "C:\Git\\fala\\buscador\\telegram_promart60-70.py"], shell=True, executable="C:\windows\system32\cmd.exe")

    subprocess.Popen([ "start", "cmd" , "/k",  "C:\Git\\fala\\buscador\\telegram_plaza70-100.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    subprocess.Popen([ "start", "cmd" , "/k",  "C:\Git\\fala\\buscador\\telegram_plaza60-70.py"], shell=True, executable="C:\windows\system32\cmd.exe")

    subprocess.Popen([ "start", "cmd" , "/k",  "C:\Git\\fala\\buscador\\telegram_cool70-100.py"], shell=True, executable="C:\windows\system32\cmd.exe")

    subprocess.Popen([ "start", "cmd" , "/k",  "C:\Git\\fala\\buscador\\telegram_tailoy70-100.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    subprocess.Popen([ "start", "cmd" , "/k",  "C:\Git\\fala\\buscador\\telegram_tailoy60-70.py"], shell=True, executable="C:\windows\system32\cmd.exe")




    ## BOTS PARA LOS COMANDOS DE LAS NAVES
    #subprocess.Popen([ "start", "cmd" , "/k", "C:\Git\\fala\\buscador\\bot_voyager.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    #subprocess.Popen([ "start", "cmd" , "/k",  "C:\Git\\fala\\buscador\\bot_discovery.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    #subprocess.Popen([ "start", "cmd" , "/k", "C:\Git\\fala\\buscador\\bot_enterprise.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    #subprocess.Popen([ "start", "cmd" , "/k", "C:\Git\\fala\\buscador\\bot_ds9.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    # subprocess.Popen([ "start", "cmd" , "/k", "C:\Git\\fala\\buscador\\bot_exelsior.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    #subprocess.Popen([ "start", "cmd" , "/k",  "C:\Git\\fala\\buscador\\bot_viper.py"], shell=True, executable="C:\windows\system32\cmd.exe")


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



