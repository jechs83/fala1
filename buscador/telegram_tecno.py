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

chat_id = config("TECNO_CHAT")
bot_token = config("TECNO_TOKEN")

bd1 = "tecno1"
bd2 = "tecno2"
dsct = 60
product  = "lentes"
category = "alterno"

db="scrap"
db_collection = "scrap"

def buscador():
  
    
    auto_telegram( category, bd1,bd2, bot_token, chat_id,dsct)

    gc.collect()

    
    buscador()
        


buscador()
