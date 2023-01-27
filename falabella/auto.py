import time
import os
from pymongo import MongoClient
from decouple import config
client = MongoClient(config("MONGO_DB"))


db = client["trigger"]
collection = db["saga"]
    
i = 0
while i == 0:

    x = collection.find( )
    
    for  e in x:
        id = e["_id"]
        status = e["status"]
            
        
        for i in range (10):
            if id ==i and status ==2:
                try:
                    os.system("C:\Git\fala\zbatch_files\saga"+i+".bat")
                except: print( "siguiente")
                
       
