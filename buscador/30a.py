from datetime import datetime
from telegram import ParseMode
from decouple import config
import telegram
import logging
import sys
import time
import os
from telegram import message
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
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
    else:
        data =  {
        "_id":"30a",     
        "status":2, 
        }
        collection.insert_one(data)
        
    time.sleep(30)
    print("YA SE TERMINO")
    print(hora)
  


i = 0
while i == 0:

    x = collection.find({"_id":"30a"})

    for  e in x:
        status = e["status"]
    x = status
    if x == 2:
        os.system("/Users/javier/GIT/fala/buscador/1.bat")
        #buscador()
