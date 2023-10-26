

from search_bot_service import  auto_telegram_between_values
from pymongo import MongoClient
from decouple import config
client = MongoClient(config("MONGO_DB"))

chat_id = config("DISCOVERY_CHAT")
bot_token = config("DISCOVERY_TOKEN")
bd1 = "discovery1"
bd2 = "discovery2"
dsct = 70
dsct2 = 100
product = "reloj"
db = client["trigger"]
collection = db["40"]
bd_name = config("db_saga")
collection_name = config("collection")
    
# def buscador():
#     try:
#      auto_telegram_between_values( bd1,bd2,bot_token, chat_id, dsct, dsct2, product,bd_name, collection_name)
#     except:
#         buscador()
    
#     buscador()

# buscador()

def buscador():
    while True:
        try:
            auto_telegram_between_values(bd1, bd2, bot_token, chat_id, dsct, dsct2, product, bd_name, collection_name)
        except Exception as e:
            print(f"An exception occurred: {e}")

# Call the function to start the infinite loop
buscador()

    