

from search_bot_service import  auto_telegram_between_values, productos_sin_dsct
from pymongo import MongoClient
from decouple import config
client = MongoClient(config("MONGO_DB"))

chat_id = config("EXCELSIOR_CHAT")
bot_token = config("LEGION_BOT")
bd1 = "excelsior1"
bd2 = "excelsior2"

product = "reloj"
db = client["trigger"]
collection = db["40"]
bd_name = config("db_ripley")
collection_name = config("collection")
    

    
def buscador():
    while True:
        try:
            productos_sin_dsct(bd1,bd2, bot_token, chat_id,bd_name,collection_name)
        except Exception as e:
            print(f"An exception occurred: {e}")

# Call the function to start the infinite loop
buscador()

    