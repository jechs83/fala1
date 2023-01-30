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
from search_bot_service import  auto_telegram, auto_telegram_total, auto_telegram_between_values
from pymongo import MongoClient
from decouple import config
client = MongoClient(config("MONGO_DB"))
TOKEN = config("ENTERPRISE_TOKEN")
chat_id = config("ENTERPRISE_CHAT_TOKEN")
bot_token = config("ENTERPRISE_TOKEN")
bd1 = "enterprise1"
bd2 = "enterprise2"
dsct = 50
dsct2 = 60

db = client["trigger"]
collection = db["40"]
    
def hora():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

def buscador():
    x = collection.find_one({"_id":0})
    if x  :
            #print(" ACTUALIZA BASE DE DATOS ")
        filter = {"_id":0}
        newvalues = { "$set":{ 
        "status":1, 
        }}
        collection.update_one(filter,newvalues)            
    else:
        data =  {
        "_id":0,     
        "status":1, 
        }
        collection.insert_one(data)

    auto_telegram_between_values( bd1,bd2,bot_token, chat_id, dsct,dsct2)


    x = collection.find_one({"_id":0})
  
    if x  :
        #print(" ACTUALIZA BASE DE DATOS ")
        filter = {"_id":0}
        newvalues = { "$set":{ 
        "status":2, 
        }}
        collection.update_one(filter,newvalues)            
   
    time.sleep(30)
    print("YA SE TERMINO")
    print(hora)
    quit()
    
  
try:
 buscador()
except:
    time.sleep(120)
    x = collection.find_one({"_id":0})
  
    if x  :
        #print(" ACTUALIZA BASE DE DATOS ")
        filter = {"_id":0}
        newvalues = { "$set":{ 
        "status":2, 
        }}
        collection.update_one(filter,newvalues)            
   
    