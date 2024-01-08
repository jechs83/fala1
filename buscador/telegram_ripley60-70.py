
from telegram_search_engine import auto_telegram_between_values
from pymongo import MongoClient
from decouple import config

client = MongoClient(config("MONGO_DB"))
chat_id = config("RIPLEY2")
bot_token = config("LLAMA_4_BOT")
collection_name = config("collection")
bd_name = config("db_ripley")

bd1 = "bd1b"
bd2 = "bd2b"
dsct = 60
dsct2 = 69

product = "reloj"
    


def buscador():
    while True:
        try:
            auto_telegram_between_values(bd1, bd2, bot_token, chat_id, dsct, dsct2,  bd_name, collection_name)
        except Exception as e:
            print(f"An exception occurred: {e}")

# Call the function to start the infinite loop
buscador()
