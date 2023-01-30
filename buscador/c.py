import time
import os
from pymongo import MongoClient
from decouple import config
import subprocess
client = MongoClient(config("MONGO_DB"))





def start():
    subprocess.Popen([ "start", "cmd" , "/k", "C:\Git\\fala\\buscador\\40.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    subprocess.Popen([ "start", "cmd" , "/k",  "C:\Git\\fala\\buscador\\auto_search_excelsior.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    subprocess.Popen([ "start", "cmd" , "/k",  "C:\Git\\fala\\buscador\\discovery.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    subprocess.Popen([ "start", "cmd" , "/k", "C:\Git\\fala\\buscador\\enterprise.py"], shell=True, executable="C:\windows\system32\cmd.exe")
    time.sleep(20*60)
    subprocess.run(["taskkill", "/IM", "cmd.exe", "/F"])
    subprocess.run(["taskkill", "/IM", "py.exe", "/F"])

    time.sleep(10)

    start()
    


def stop():
    subprocess.run(["taskkill", "/IM", "py.exe", "/F"])
    time.sleep(10)
    
    
start()



