
from decouple import config
from search_bot_service import  auto_telegram_between_values
from pymongo import MongoClient
from decouple import config
from pymongo import MongoClient
from decouple import config
client = MongoClient(config("MONGO_DB"))


chat_id = config("OH2")
bot_token = config("LLAMA_6_BOT")
bd1 = "bd1"
bd2 = "bd2"
dsct = 60
dsct2 = 69
product = "reloj"
db = client["trigger"]
collection = db["40"]
bd_name = config("db_oechsle")
collection_name = config("collection")
    


def buscador():
    while True:
        try:
            auto_telegram_between_values(bd1, bd2, bot_token, chat_id, dsct, dsct2, product, bd_name, collection_name)
            auto_telegram_between_values(bd1, bd2, bot_token, chat_id, dsct, dsct2, product, "wong", collection_name)
            auto_telegram_between_values(bd1, bd2, bot_token, chat_id, dsct, dsct2, product, "shopstar", collection_name)
            auto_telegram_between_values(bd1, bd2, bot_token, chat_id, dsct, dsct2, product, "coolbox", collection_name)

        except Exception as e:
            print(f"An exception occurred: {e}")

# Call the function to start the infinite loop
buscador()
