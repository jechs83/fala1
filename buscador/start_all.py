import time
import subprocess
from pymongo import MongoClient
from decouple import config

client = MongoClient(config("MONGO_DB"))


## SOLO FUNCIONA  EN WINDOWS 
def start():

    ##  BUSCADORES DE BASE DE DATOS  - ENVIA A TELGRAM LAS OFERTAS 
    bot1 = "telegram_ripley70-100.py"
    bot2= "telegram_saga70-100.py"
    bot3= "telegram_curacao70-100.py"
    bot4= "telegram_oh70-100.py"

    bot5= "telegram_promart70-100.py"
    bot6= "telegram_plaza70-100.py"
    bot7= "telegram_tailoy70-100.py"
    
    bot8= "telegram_platano70-100.py"
    bot9= "telegram_product-sindsct.py"
    
    lista = [bot1,bot2,bot3,bot4,bot5,bot6,bot7,bot8,bot9]

    for i in lista:
        subprocess.Popen([ "start", "cmd" , "/k", "C:\Git\\fala\\buscador\\"+i], shell=True, executable="C:\windows\system32\cmd.exe")
    time.sleep(900) 

    ## MATGA TODOS LOS PROCESOS ANTES DE REINICIAR LA FUNCION START 
    subprocess.run(["taskkill", "/IM", "cmd.exe", "/F"])
    subprocess.run(["taskkill", "/IM", "py.exe", "/F"])
    time.sleep(5)

    start()
    
def stop():
    subprocess.run(["taskkill", "/IM", "py.exe", "/F"])
    time.sleep(10)
    
     

start()




