from datetime import datetime
from decouple import config
from search_bot_service import  auto_telegram
from pymongo import MongoClient
from decouple import config


client = MongoClient(config("MONGO_DB"))
TOKEN = config("RICHI_BOY_TOKEN")
chat_id = config("USS_DEFIANT")
bot_token = config("RICHI_BOY_TOKEN")

bd1 = "richi1"
bd2 = "richi2"
dsct = 60
product  = "lentes"
category = "alterno"
db="scrap"
db_collection = "scrap"
    
def hora():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time



def buscador():
  
    auto_telegram( category, bd1,bd2, bot_token, chat_id,dsct)

    buscador()
        
buscador()
