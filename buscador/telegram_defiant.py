from datetime import datetime
from decouple import config
from search_bot_service import  auto_telegram_between_values
from pymongo import MongoClient


client = MongoClient(config("MONGO_DB"))
chat_id = config("DEFIANT_CHAT")
bot_token = config("DEFIANT_TOKEN")

bd1 = "defiant1"
bd2 = "defiant2"
dsct = 80
dsct2 = 1000
product  = "lentes"
category = "alterno"
db="scrap"
db_collection = "scrap"
    
def hora():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time



def buscador():
    
    auto_telegram_between_values(  bd1,bd2, bot_token, chat_id,dsct, dsct2, product)


    buscador()
    

        
buscador()
