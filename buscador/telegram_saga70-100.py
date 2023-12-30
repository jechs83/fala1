from search_bot_service import  auto_telegram_between_values
from pymongo import MongoClient
from decouple import config

client = MongoClient(config("MONGO_DB"))
chat_id = config("SAGA1")
bot_token = config("LLAMA_1_BOT")
collection_name = config("collection")
bd_name = config("db_saga")

bd1 = "bd1"
bd2 = "bd2"
dsct = 70
dsct2 = 100

product = "reloj"
db = client["trigger"]
collection = db["40"]


    
def buscador():
    while True:
        try:
            auto_telegram_between_values(bd1, bd2, bot_token, chat_id, dsct, dsct2, product, bd_name, collection_name)
        except Exception as e:
            print(f"An exception occurred: {e}")

# Call the function to start the infinite loop
buscador()

