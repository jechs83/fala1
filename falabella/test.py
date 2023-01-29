
from pymongo import MongoClient
import os
import sys
import time
from decouple import config
import subprocess

client = MongoClient(config("MONGO_DB"))

array = ["knasta", "ripley", "saga", "curacao", "shop", "tailoy"]

def restart():

    try:
        subprocess.run(["taskkill", "/IM", "WindowsTerminal.exe", "/F"])
    except: print(" no hay terminal abierto")
    time.sleep(10)
    subprocess.Popen(["start", "C:\GIT\\fala\\curacao\\auto.py"] ,shell=True, executable="C:\WINDOWS\system32\cmd.exe")
    subprocess.Popen(["start", "C:\GIT\\fala\\falabella\\auto.py"] ,shell=True, executable="C:\WINDOWS\system32\cmd.exe")
    subprocess.Popen(["start", "C:\GIT\\fala\\ripley\\auto.py"] ,shell=True, executable="C:\WINDOWS\system32\cmd.exe")
    subprocess.Popen(["start", "C:\GIT\\fala\\knasta\\auto.py"] ,shell=True, executable="C:\WINDOWS\system32\cmd.exe")
    subprocess.Popen(["start", "C:\GIT\\fala\\tayloy\\auto.py"] ,shell=True, executable="C:\WINDOWS\system32\cmd.exe")
    subprocess.Popen(["start", "C:\GIT\\fala\\shopstar\\auto.py"] ,shell=True, executable="C:\WINDOWS\system32\cmd.exe")
    






    def bd_change(num, bd_status, market ):
        
        db = client["trigger"]
        collection = db[market]
        
        
        x = collection.find_one({"_id":num})
        if x  :
                #print(" ACTUALIZA BASE DE DATOS ")
            filter = {"_id":num}
            newvalues = { "$set":{ 
            "status":bd_status, 
            }}
            collection.update_one(filter,newvalues)      

        

        
    for idx, val in enumerate(array):
        
        for i in range (10):
            bd_change(i, 2, str(val) )


def stop ():
    try:
     subprocess.run(["taskkill", "/IM", "WindowsTerminal.exe", "/F"])
    except: print("no hay terminal abierto")
    time.sleep(5)
    try:
     subprocess.run(["taskkill", "/IM", "WindowsTerminal.exe", "/F"])
    except: print("no hay terminal abierto")
    
    try:
     subprocess.run(["taskkill", "/IM", "python.exe", "/F"])
    except: print("no hay terminal abierto")
    





arg_ = sys.argv[1]


if arg_ == "restart":
    restart()

if arg_ == "stop":
    stop()
    

    
    