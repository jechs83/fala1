
from search_bot_service import  auto_telegram
from pymongo import MongoClient
from decouple import config
from telegram_search_engine import auto_telegram_between_values


client = MongoClient(config("MONGO_DB"))
chat_id = "-1001951603431"
bot_token = "6571641209:AAEAGNpFahbGeFCRzz27b7V7mXmJx-R5Etc" #somos_borg

bd1 = "bd1b"
bd2 = "bd2b"
dsct = 60
dsct2 = 100
product = "reloj"
db = client["trigger"]
collection = db["40"]
bd_name = "juntoz"
collection_name = "scrap"
    


def buscador():
    while True:
        try:
            auto_telegram_between_values(bd1, bd2, bot_token, chat_id, dsct, dsct2,  bd_name, collection_name)
        except Exception as e:
            print(f"An exception occurred: {e}")

# Call the function to start the infinite loop
buscador()

