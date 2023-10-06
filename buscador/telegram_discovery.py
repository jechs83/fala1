from datetime import datetime
from decouple import config
from search_bot_service import  auto_telegram, auto_telegram_total, auto_telegram_between_values
from pymongo import MongoClient
from decouple import config
client = MongoClient(config("MONGO_DB"))

chat_id = config("DISCOVERY_CHAT")
bot_token = config("DISCOVERY_TOKEN")
bd1 = "discovery1"
bd2 = "discovery2"
dsct = 70
dsct2 = 101
product = "reloj"
db = client["trigger"]
collection = db["40"]
    
def hora():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

def buscador():

    try:
     auto_telegram_between_values( bd1,bd2,bot_token, chat_id, dsct, dsct2, product)
    except:
        buscador()
    buscador()
buscador()

    