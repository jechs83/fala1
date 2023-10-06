
from search_bot_service import   auto_telegram_between_values
from pymongo import MongoClient
from decouple import config

client = MongoClient(config("MONGO_DB"))
chat_id = config("VOYAGER_CHAT")
bot_token = config("VOYAGER_TOKEN")


bd1 = "voyager1"
bd2 = "voyager2"

dsct = 70
dsct2 = 80
product  = "lentes"
category = "tecno"

db="scrap"
db_collection = "scrap"
    

def buscador():
    
    auto_telegram_between_values(  bd1,bd2, bot_token, chat_id,dsct, dsct2, product)


    buscador()
    

        
buscador()


# dsct = 70
# dsct2 = 101

# db = client["trigger"]
# collection = db["60"]
    
# def hora():
#     now = datetime.now()
#     current_time = now.strftime("%H:%M:%S")
#     return current_time

# def buscador():
 
#     try:
#      auto_telegram_between_values( bd1,bd2,bot_token, chat_id, dsct,dsct2, "reloj")
#     except:
#         buscador()
#     buscador()


# buscador()
    