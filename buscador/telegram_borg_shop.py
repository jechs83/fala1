

from search_bot_service import  auto_telegram_between_values, productos_sin_dsct
from pymongo import MongoClient
from decouple import config
client = MongoClient(config("MONGO_DB"))

chat_id = "-1001951603431"
bot_token = "6960852622:AAHDsUlDu6BAMabCUb_6nt_vFxTtKW_3IOI"
bd1 = "discovery1"
bd2 = "discovery2"

product = "reloj"
db = client["trigger"]
collection = db["40"]
#bd_name = config("db_saga")
collection_name = config("collection")
    

    
def buscador():
    while True:
        try:
            # productos_sin_dsct(bd1,bd2, bot_token, chat_id,bd_name,collection_name)
            productos_sin_dsct(bd1,bd2, bot_token, chat_id,"shopstar",collection_name)
      
        except Exception as e:
            print(f"An exception occurred: {e}")

# Call the function to start the infinite loop
buscador()

    