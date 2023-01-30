import time
import os
from pymongo import MongoClient
from decouple import config
import subprocess
client = MongoClient(config("MONGO_DB"))


db = client["trigger"]
collection = db["40"]
    
i = 0
while i == 0:

    x = collection.find({"_id":0})

    for  e in x:
        status = e["status"]
    x = status
    if x == 2:
        subprocess.Popen([ "start", "C:\Git\\fala\\buscador\\40.py"], shell=True, executable="C:\windows\system32\cmd.exe")
        time.sleep()
        #buscador()
