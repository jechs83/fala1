from datetime import datetime
from decouple import config
from search_bot_service import  auto_telegram, auto_telegram_total, auto_telegram_between_values
from decouple import config
#client = MongoClient(config("MONGO_DB"))

chat_id = config("ENTERPRISE_CHAT")
bot_token = config("ENTERPRISE_TOKEN")
bd1 = "enterprise1"
bd2 = "enterprise2"
dsct = 50
dsct2 = 100
db="scrap"
db_collection = "scrap"
product = "lentes"
    
def hora():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

def buscador():
 
    try:
     auto_telegram_between_values( bd1,bd2,bot_token, chat_id, dsct,dsct2, "lentes")
    except:
        buscador()
    
    buscador()


buscador()
    