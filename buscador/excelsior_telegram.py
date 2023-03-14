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
from search_bot_service import  auto_telegram, auto_telegram_total,auto_telegram_between_values,auto_telegram_between_values_custom_bd
from pymongo import MongoClient
from decouple import config
client = MongoClient(config("MONGO_DB"))
TOKEN = config("CAPITAN_PIKE_TOKEN")
chat_id = config("EXCELSIOR_CHAT_TOKEN")
bot_token = config("CAPITAN_PIKE_TOKEN")
bd1 = "excelsior1"
bd2 = "excelsior2"
dsct = 80
dsct2 = 101
product  = "lentes"

db="scrap"
db_collection = "scrap"
    
def hora():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

def buscador():
  
    
    auto_telegram_between_values_custom_bd( bd1,bd2,bot_token, chat_id, dsct, dsct2, product, db, db_collection)
   
        
        ###############
    db1 = client["scrap"]
    collection1 = db1["excelsior"]

    x = collection1.find_one({"_id":0})
      
    
    if x  :
            #print(" ACTUALIZA BASE DE DATOS ")
            filter = {"_id":0}
            newvalues = { "$set":{ 
                 "_id":0,
            "status":0,   
        
            }}
            collection1.update_one(filter,newvalues)
            
    else:
            data =  {
                
                "_id":0,
                "status":1
                }
            collection1.insert_one(data)
    
    
    print("se guardo en bd status de buqueda")

        
    buscador() 
    

buscador()
