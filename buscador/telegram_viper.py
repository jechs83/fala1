from decouple import config
from search_bot_service import  auto_telegram
from pymongo import MongoClient
from decouple import config

client = MongoClient(config("MONGO_DB"))
chat_id = config("VIPER_CHAT")
bot_token = config("VIPER_TOKEN")
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
