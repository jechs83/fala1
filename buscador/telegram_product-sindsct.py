

from telegram_search_engine import productos_sin_dsct
from pymongo import MongoClient
from decouple import config
client = MongoClient(config("MONGO_DB"))

chat_id = config("TEST1")
bot_token = config("LLAMA_15_BOT")
bd1 = "bd1"
bd2 = "bd2"

collection_name = config("collection")
    

    
def buscador():
    while True:
        try:   
            productos_sin_dsct(bd1,bd2, bot_token, chat_id,"saga",collection_name)
            productos_sin_dsct(bd1,bd2, bot_token, chat_id,"ripley",collection_name)
            productos_sin_dsct(bd1,bd2, bot_token, chat_id,"plazavea",collection_name)
            productos_sin_dsct(bd1,bd2, bot_token, chat_id,"promart",collection_name)
            productos_sin_dsct(bd1,bd2, bot_token, chat_id,"tailoy",collection_name)
            productos_sin_dsct(bd1,bd2, bot_token, chat_id,"curacao",collection_name)
            productos_sin_dsct(bd1,bd2, bot_token, chat_id,"platanitos",collection_name)
            productos_sin_dsct(bd1,bd2, bot_token, chat_id,"oechsle",collection_name)
            productos_sin_dsct(bd1,bd2, bot_token, chat_id,"shopstar",collection_name)
            productos_sin_dsct(bd1,bd2, bot_token, chat_id,"wong",collection_name)
            productos_sin_dsct(bd1,bd2, bot_token, chat_id,"metro",collection_name)
           
         
            
        except Exception as e:
            print(f"An exception occurred: {e}")

# Call the function to start the infinite loop
buscador()

    