
from decouple import config
from telegram_search_engine import auto_telegram_between_values
from pymongo import MongoClient
from decouple import config
from pymongo import MongoClient
from decouple import config

client = MongoClient(config("MONGO_DB"))
#chat_id = config("VEA1")
bot_token = "6596853396:AAGsQ8G_hIOvSPKTXUnt0WWtNJkITcACkE8" #llama bot 7
chat_id = "-1002103101431"




bd1 = "bd1"
bd2 = "bd2"
dsct = 60
dsct2 = 100
product = "reloj"
db = client["trigger"]
collection = db["40"]
bd_name = config("db_plazavea")
collection_name = config("collection")
    


def buscador():
    while True:
        try:
            auto_telegram_between_values(bd1, bd2, bot_token, chat_id, dsct, dsct2, bd_name, collection_name)
        except Exception as e:
            print(f"An exception occurred: {e}")

# Call the function to start the infinite loop
buscador()
