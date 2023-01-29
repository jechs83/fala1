import time
import os
import subprocess 
from pymongo import MongoClient
from decouple import config

client = MongoClient(config("MONGO_DB"))


db = client["trigger"]
collection = db["saga"]


def bd_change(num, bd_status):
    
    x = collection.find_one({"_id":int(num)})
    if x  :
            #print(" ACTUALIZA BASE DE DATOS ")
        filter = {"_id":int(num)}
        newvalues = { "$set":{ 
        "status":bd_status, 
        }}
        collection.update_one(filter,newvalues)      
    
    
def loop():
    x = collection.find( )
    
    for  e in x:
        id = e["_id"]
        status = e["status"]
        
        for i in range (10):
            if id ==i and status ==2:
                try:
                    subprocess.Popen([ "start", "C:\\GIT\\fala\\falabella\\saga.py", str(i)], shell=True, executable="C:\WINDOWS\system32\cmd.exe")
                    bd_change(i, 1)
                    print("proceso "+str(i))
                   
                except: 
                    print( "siguiente")
                    bd_change(i, 2)
                            
                  
i = 0
while i == 0:   
    loop() 
