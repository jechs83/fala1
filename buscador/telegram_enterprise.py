
from search_bot_service import auto_telegram_between_values
from decouple import config

chat_id = config("ENTERPRISE_CHAT")
bot_token = config("ENTERPRISE_TOKEN")
bd1 = "enterprise1"
bd2 = "enterprise2"
dsct = 30
dsct2 = 60
db="scrap"
db_collection = "scrap"
product = "lentes"
    

def buscador():
 
    try:
     auto_telegram_between_values( bd1,bd2,bot_token, chat_id, dsct,dsct2, "lentes")
    except:
        buscador()
    
    buscador()


buscador()
    