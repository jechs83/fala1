
from decouple import config
from search_bot_service import  auto_telegram_between_values
from pymongo import MongoClient
from decouple import config
from pymongo import MongoClient
from decouple import config
import gc
client = MongoClient(config("MONGO_DB"))


# chat_id = config("OH_CHAT_70-100")
# bot_token = config("PIKE_BOT_TOKEN")
chat_id = "-4090886629"
bot_token = "6663439593:AAG2g51K4hlWF4Upt8qEqSUK8JRSQBSIQFM"
bd1 = "enterprise1"
bd2 = "enterprise2"
dsct = 60
dsct2 = 100
product = "reloj"
db = client["trigger"]
collection = db["40"]
bd_name = config("db_coolbox")
collection_name = config("collection")
    


def buscador():
    while True:
        try:
            #auto_telegram_between_values(bd1, bd2, bot_token, chat_id, dsct, dsct2, product, "shopstar", collection_name)
            auto_telegram_between_values(bd1, bd2, bot_token, chat_id, dsct, dsct2, product, "platanitos", collection_name)
            auto_telegram_between_values(bd1, bd2, bot_token, chat_id, dsct, dsct2, product, "hiraoka", collection_name)
            # auto_telegram_between_values(bd1, bd2, bot_token, chat_id, dsct, dsct2, product, "wong", collection_name)
            gc.collect()

        except Exception as e:
            print(f"An exception occurred: {e}")

# Call the function to start the infinite loop
buscador()
