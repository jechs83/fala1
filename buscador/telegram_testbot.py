
from search_bot_service import  auto_telegram_category,productos_sin_dsct
from pymongo import MongoClient
from decouple import config

client = MongoClient(config("MONGO_DB"))
chat_id = config("R2D2_CHAT")
bot_token = config("R2D2_TOKEN")
bd1 = "nameless1"
bd2 = "nameless2"
dsct = 80
dsct2 = 100
product  = "lentes"
category = "alterno"

db="scrap"
db_collection = "scrap"
def buscador():
    #auto_telegram_category( category, bd1,bd2,bot_token, chat_id,dsct)
    productos_sin_dsct(bd1,bd2, bot_token, chat_id)
        
    buscador() 
    

buscador()
