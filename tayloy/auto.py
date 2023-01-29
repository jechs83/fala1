import time
import os
import subprocess
from pymongo import MongoClient
from decouple import config
client = MongoClient(config("MONGO_DB"))


db = client["trigger"]
collection = db["tailoy"]
    

def loop():
    x = collection.find( )
    
    for  e in x:
        id = e["_id"]
        status = e["status"]
        
        for i in range (2):
            if id ==i and status ==2:
                try:
                    subprocess.Popen([ "start", "C:\\GIT\\fala\\tayloy\\tailoy.py", str(i)], shell=True, executable="C:\WINDOWS\system32\cmd.exe")
                    print(i)


                    #os.system("python C:\GIT\fala\falabella\saga.py "+str(i))
        
                except: print( "siguiente")
            
            
             
                
i = 0
while i == 0:   
    loop() 
