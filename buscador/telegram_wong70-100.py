
from decouple import config
from telegram_search_engine import auto_telegram_between_values
from pymongo import MongoClient
from decouple import config
from pymongo import MongoClient
from decouple import config
client = MongoClient(config("MONGO_DB"))


#chat_id = config("OH1")

bot_token = "6922871886:AAHzi7r3WQYUBx2-CI7fcENdfN_uoKSgIo8"
chat_id="-1001538602771"



#chat_id = "-4264798075"
#bot_token = "7094750871:AAEIk-LQRXkg7eeTUKFPiVaHUVlu9TWIO7Y"
#collection_name = config("collection")

bd1 = "bd1"
bd2 = "bd2"
dsct = 60
dsct2 = 100
product = "reloj"
db = client["trigger"]
collection = db["40"]
bd_name = config("db_oechsle")
collection_name = config("collection")
    


def buscador():
    while True:
        try:
            auto_telegram_between_values(bd1, bd2, bot_token, chat_id, dsct, dsct2,  "wong", collection_name)
            auto_telegram_between_values(bd1, bd2, bot_token, chat_id, dsct, dsct2,  "metro", collection_name)
            auto_telegram_between_values(bd1, bd2, bot_token, chat_id, dsct, dsct2,  "hiraoka", collection_name)
            auto_telegram_between_values(bd1, bd2, bot_token, chat_id, dsct, dsct2,  "coolbox", collection_name)

        except Exception as e:
            print(f"An exception occurred: {e}")

# Call the function to start the infinite loop
buscador()
