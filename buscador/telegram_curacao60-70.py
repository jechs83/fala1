

from decouple import config
from telegram_search_engine import auto_telegram_between_values
from pymongo import MongoClient
from decouple import config
from pymongo import MongoClient
import time
from decouple import config
client = MongoClient(config("MONGO_DB"))
chat_id = config("CURACAO2") 
bot_token = config("LLAMA_10_BOT") 


bd1 = "bd1b"
bd2 = "bd2b"
dsct = 60
dsct2 = 69
product = "reloj"
db = client["trigger"]
collection = db["40"]
bd_name = config("db_curacao")
collection_name = config("collection")


def buscador():
    
    while True:
        try:
            auto_telegram_between_values(bd1, bd2, bot_token, chat_id, dsct, dsct2,  bd_name, collection_name)
            auto_telegram_between_values(bd1, bd2, bot_token, chat_id, dsct, dsct2,  "hiraoka", collection_name)
            auto_telegram_between_values(bd1, bd2, bot_token, chat_id, dsct, dsct2,  "platanitos", collection_name)


        except Exception as e:
            print(f"An exception occurred: {e}")

# Call the function to start the infinite loop
buscador()
