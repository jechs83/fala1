
from search_bot_service import  auto_telegram
from pymongo import MongoClient
from decouple import config

client = MongoClient(config("MONGO_DB"))
chat_id = config("TECNO_CHAT")
bot_token = config("TECNO_TOKEN")

bd1 = "tecno1"
bd2 = "tecno2"
dsct = 80
product  = "lentes"
category = "alterno"

db="saga"
db_collection = "scrap"

def buscador():
  
    try:
        auto_telegram( category, bd1,bd2, bot_token, chat_id,dsct)
    except: 
        buscador()
    
    buscador()

buscador()
