from datetime import datetime
from decouple import config
import telegram
import logging
import sys
import gc
import time
import os
from telegram import message
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from search_bot_service import  auto_telegram
from pymongo import MongoClient
from decouple import config
client = MongoClient(config("MONGO_DB"))
TOKEN = "6049509542:AAEBPgX9OLC6ZFNsJRe1JFugqz3PZOADEjE"

#chat_id = config("RICHI_CHAT_TOKEN")
chat_id = config("EXCELSIOR_CHAT_TOKEN")
bot_token = "6049509542:AAEBPgX9OLC6ZFNsJRe1JFugqz3PZOADEjE"

bd1 = "tecno1"
bd2 = "tecno2"
dsct = 60
product  = "lentes"
category = "tecno"

db="scrap"
db_collection = "scrap"
    
def hora():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

def buscador():
  
    
    auto_telegram( category, bd1,bd2, bot_token, chat_id,dsct)

    gc.collect()

    
    buscador()
        


buscador()
