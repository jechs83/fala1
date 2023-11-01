

from search_bot_service import  auto_telegram_between_values
from pymongo import MongoClient
from decouple import config
client = MongoClient(config("MONGO_DB"))

chat_id = config("CHAT_ID")
bot_token = config("BOT_TOKEN_SHOP1")



bd1 = "shop1"
bd2 = "shop2"
dsct = 70
dsct2 = 100
product = "reloj"
db = client["trigger"]
collection = db["40"]
bd_name = config("db_shop")
collection_name = config("collection")
    

def buscador():
    while True:
        try:
            auto_telegram_between_values(bd1, bd2, bot_token, chat_id, dsct, dsct2, product, bd_name, collection_name)
        except Exception as e:
            print(f"An exception occurred: {e}")

# Call the function to start the infinite loop
buscador()

    
