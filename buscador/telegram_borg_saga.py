

from search_bot_service import  auto_telegram_between_values, productos_sin_dsct
from pymongo import MongoClient
from decouple import config
client = MongoClient(config("MONGO_DB"))

chat_id = config("DISCOVERY_CHAT")
bot_token = config("SOMOS_BORG_BOT_TOKEN")
bd1 = "discovery1"
bd2 = "discovery2"

product = "reloj"
db = client["trigger"]
collection = db["40"]
bd_name = config("db_saga")
collection_name = config("collection")
    

    
def buscador():
    while True:
        try:
            # productos_sin_dsct(bd1,bd2, bot_token, chat_id,bd_name,collection_name)
            productos_sin_dsct(bd1,bd2, bot_token, chat_id,"platanitos",collection_name)
            productos_sin_dsct("enterprise1","enterprise2", bot_token, chat_id,"promart",collection_name)
            productos_sin_dsct("enterprise1","enterprise2", bot_token, chat_id,"tailoy",collection_name)
        except Exception as e:
            print(f"An exception occurred: {e}")

# Call the function to start the infinite loop
buscador()

    