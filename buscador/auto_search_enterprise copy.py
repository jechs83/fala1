from datetime import datetime
from decouple import config
import sys
import time
from search_bot_service import  auto_telegram


TOKEN = config("ENTERPRISE_TOKEN")
chat_id = config("ENTERPRISE_CHAT_TOKEN")
bot_token = config("ENTERPRISE_TOKEN")
bd1 = "enterprise1"
bd2 = "enterprise2"
porcentage = 70

def hora():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

def buscador():
    auto_telegram("electro", bd1,bd2,bot_token, chat_id, porcentage)

    auto_telegram("tecno", bd1,bd2,bot_token, chat_id,porcentage)

    auto_telegram("juguetes", bd1,bd2,bot_token, chat_id,porcentage)

    auto_telegram("ropa", bd1,bd2,bot_token, chat_id,porcentage)

    auto_telegram("bicicleta", bd1,bd2,bot_token, chat_id,porcentage)

    auto_telegram("celular", bd1,bd2,bot_token, chat_id,porcentage)

    auto_telegram("herramientas", bd1,bd2,bot_token, chat_id,porcentage)

    print("se pausa 10 min")
    print(hora())
    time.sleep(5*60) #this will stop the program for 10 minutes

    buscador()


buscador()
