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

db="scrap2"
db_collection = "scrap2"
    
def hora():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

def buscador():
  
    try:
     auto_telegram_between_values_custom_bd( bd1,bd2,bot_token, chat_id, dsct, dsct2, product, db, db_collection)

    except:
        buscador()
    buscador()

buscador()