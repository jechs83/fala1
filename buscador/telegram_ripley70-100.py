
from decouple import config
from telegram_search_engine import auto_telegram_between_values
from pymongo import MongoClient
from decouple import config
from pymongo import MongoClient
from decouple import config
client = MongoClient(config("MONGO_DB"))


#chat_id = config("RIPLEY1")

#chat_id = "-1001852480744"
#bot_token = config("LLAMA_3_BOT")


chat_id = "-4264798075"
bot_token = "7094750871:AAEIk-LQRXkg7eeTUKFPiVaHUVlu9TWIO7Y"
collection_name = config("collection")
bd1 = "bd1"
bd2 = "bd2"
dsct =  70
dsct2 = 100

db = client["trigger"]
collection = db["40"]
bd_name = config("db_ripley")
collection_name = config("collection")
    


def buscador():
    while True:
        try:
            auto_telegram_between_values(bd1, bd2, bot_token, chat_id, dsct, dsct2, bd_name, collection_name)
        except Exception as e:
            print(f"An exception occurred: {e}")

# Call the function to start the infinite loop
buscador()
