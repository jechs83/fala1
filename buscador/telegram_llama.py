
from decouple import config
from search_bot_service import  auto_telegram_between_values
from pymongo import MongoClient
from decouple import config
from pymongo import MongoClient
from decouple import config
client = MongoClient(config("MONGO_DB"))


# chat_id = config("OH_CHAT_70-100")
# bot_token = config("PIKE_BOT_TOKEN")
chat_id = "-1002036942471"
bot_token = "6658278408:AAHEdP3DC31bN81p0KUxlDbaJZsZt95Vy0U"
bd1 = "bd1"
bd2 = "bd2"
dsct = 64
dsct2 = 65
product = "reloj"
db = client["trigger"]
collection = db["40"]
bd_name = "cuponmania"
collection_name = config("collection")
    


def buscador():
    while True:
        try:
            #auto_telegram_between_values(bd1, bd2, bot_token, chat_id, dsct, dsct2, product, "saga", collection_name)
            auto_telegram_between_values(bd1, bd2, bot_token, chat_id, dsct, dsct2, product, "ripley", collection_name)
            #auto_telegram_between_values(bd1, bd2, bot_token, chat_id, dsct, dsct2, product, "tailoy", collection_name)
            #auto_telegram_between_values(bd1, bd2, bot_token, chat_id, dsct, dsct2, product, "curacao", collection_name)
            #auto_telegram_between_values(bd1, bd2, bot_token, chat_id, dsct, dsct2, product, "plazavea", collection_name)
            #auto_telegram_between_values(bd1, bd2, bot_token, chat_id, dsct, dsct2, product, "oechsle", collection_name)
            # auto_telegram_between_values(bd1, bd2, bot_token, chat_id, dsct, dsct2, product, "promart", collection_name)
        except Exception as e:
            print(f"An exception occurred: {e}")

# Call the function to start the infinite loop
buscador()
