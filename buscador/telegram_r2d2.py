from datetime import datetime

from decouple import config
from telegram import message
from search_bot_service import  auto_telegram, auto_telegram_total,auto_telegram_between_values,auto_telegram_between_values_custom_bd
from pymongo import MongoClient
from decouple import config
client = MongoClient(config("MONGO_DB"))

TOKEN = config("SOMOS_BORG_BOT")
#chat_id = config("NAME_LESS_TOKEN")
chat_id = -1001951603431
bot_token = config("SOMOS_BORG_BOT")
bd1 = "nameless1"
bd2 = "nameless2"
dsct = 70
dsct2 = 100
product  = "lentes"

db="scrap"
db_collection = "scrap"
    
def hora():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

def buscador():
  
    
    auto_telegram_between_values_custom_bd( bd1,bd2,bot_token, chat_id, dsct, dsct2, product, db, db_collection)
        
    buscador() 
    

buscador()
