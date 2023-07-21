from decouple import config
from search_bot_service import  auto_telegram
from pymongo import MongoClient
from decouple import config

client = MongoClient(config("MONGO_DB"))
TOKEN = config("VIPER_BOT_TOKEN")
chat_id = config("NAME_LESS_TOKEN")
bot_token = config("VIPER_BOT_TOKEN")
bd1 = "viper1"
bd2 = "viper2"
dsct = 60
product  = "lentes"
category = "alterno"

db="scrap"
db_collection = "scrap"
    

def buscador():
  
    
    auto_telegram( category, bd1,bd2, bot_token, chat_id,dsct)

    buscador()
        


buscador()
