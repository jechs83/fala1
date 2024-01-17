
from decouple import config
from telegram_search_engine import auto_telegram_between_values
from pymongo import MongoClient
from decouple import config
from pymongo import MongoClient
import time
from decouple import config
client = MongoClient(config("MONGO_DB"))


# chat_id = config("OH_CHAT_70-100")
# bot_token = config("PIKE_BOT_TOKEN")
chat_id = "-1002046813958"
bot_token = "6794925800:AAExqiVDl3UeGEopEhRMAqDPrqQYF6M_1bg"
bd1 = "cupon"
bd2 = "cupon"
dsct = 70
dsct2 = 100

collection_name = config("collection")

#collection_name = "otros"

    


def buscador():
    while True:

    
        try:
            # auto_telegram_between_values(bd1, bd2, bot_token, chat_id, dsct, dsct2, "wong", collection_name)
            auto_telegram_between_values(bd1, bd2, bot_token, chat_id, dsct, dsct2, "saga", collection_name)
            auto_telegram_between_values(bd1, bd2, bot_token, chat_id, dsct, dsct2, "ripley", collection_name)
            print("esperando 1 hora")
            time.sleep(60*60)

        except Exception as e:
            print(f"An exception occurred: {e}")

    

# Call the function to start the infinite loop
buscador()
