import time
import os
from pymongo import MongoClient
from decouple import config
client = MongoClient(config("MONGO_DB"))


db = client["trigger"]
collection = db["30"]
    
i = 0
while i == 0:

    x = collection.find({"_id":"30a"})

    for  e in x:
        status = e["status"]
    x = status
    if x == 2:
        os.system("C:\Git\\fala\\buscador\\1.bat")
        time.sleep(40)
        #buscador()
        
        
    
