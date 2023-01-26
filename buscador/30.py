from datetime import datetime
from decouple import config
import time
from search_bot_service import  auto_telegram, auto_telegram_total
from pymongo import MongoClient
from decouple import config
client = MongoClient(config("MONGO_DB"))

TOKEN = config("CAPITAN_SPOK_TOKEN")
chat_id = config("DISCOVERY_CHAT_TOKEN")
bot_token = config("CAPITAN_SPOK_TOKEN")
bd1 = "discovery1"
bd2 = "discovery2"
dsct = 70

db = client["trigger"]
collection = db["30"]
    
def hora():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

def buscador():
    x = collection.find_one({"_id":"30a"})
    if x  :
            #print(" ACTUALIZA BASE DE DATOS ")
        filter = {"_id":"30a"}
        newvalues = { "$set":{ 
        "status":1, 
        }}
        collection.update_one(filter,newvalues)            
    else:
        data =  {
        "_id":"30a",     
        "status":1, 
        }
        collection.insert_one(data)

    auto_telegram_total( bd1,bd2,bot_token, chat_id, dsct)


    x = collection.find_one({"_id":"30a"})
  
    if x  :
        #print(" ACTUALIZA BASE DE DATOS ")
        filter = {"_id":"30a"}
        newvalues = { "$set":{ 
        "status":2, 
        }}
        collection.update_one(filter,newvalues)            

    print("YA SE TERMINO")
    print(hora)

try:
    buscador()
except:
    x = collection.find_one({"_id":"30a"})
  
    if x  :
        #print(" ACTUALIZA BASE DE DATOS ")
        filter = {"_id":"30a"}
        newvalues = { "$set":{ 
        "status":2, 
        }}
        collection.update_one(filter,newvalues)            
   