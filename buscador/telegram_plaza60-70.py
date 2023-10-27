
from decouple import config
from search_bot_service import  auto_telegram_between_values
from pymongo import MongoClient
from decouple import config
from pymongo import MongoClient
from decouple import config
client = MongoClient(config("MONGO_DB"))


# chat_id = config("OH_CHAT_70-100")
# bot_token = config("PIKE_BOT_TOKEN")
chat_id = "-4052168394"
bot_token = "6747921067:AAG0frH1swAvpVjn_nc4mQ2ND_dm014njLI"
bd1 = "enterprise1"
bd2 = "enterprise2"
dsct = 60
dsct2 = 69
product = "reloj"
db = client["trigger"]
collection = db["40"]
bd_name = config("db_plazavea")
collection_name = config("collection")
    


def buscador():
    while True:
        try:
            auto_telegram_between_values(bd1, bd2, bot_token, chat_id, dsct, dsct2, product, bd_name, collection_name)
        except Exception as e:
            print(f"An exception occurred: {e}")

# Call the function to start the infinite loop
buscador()
