from datetime import datetime
from telegram import ParseMode
from decouple import config
import telegram
import logging
import sys
import time
from telegram import message
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from search_bot_service import  auto_telegram



TOKEN = config("CAPITAN_SPOK_TOKEN")
chat_id = config("DISCOVERY_CHAT_TOKEN")
bot_token = config("CAPITAN_SPOK_TOKEN")
bd1 = "discovery1"
bd2 = "discovery2"

def hora():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

def buscador():
    auto_telegram("electro", bd1,bd2,bot_token, chat_id)

    auto_telegram("tecno", bd1,bd2,bot_token, chat_id)

    auto_telegram("juguetes", bd1,bd2,bot_token, chat_id)

    auto_telegram("ropa", bd1,bd2,bot_token, chat_id)

    auto_telegram("bicicleta", bd1,bd2,bot_token, chat_id)

    auto_telegram("celular", bd1,bd2,bot_token, chat_id)

    auto_telegram("herramientas", bd1,bd2,bot_token, chat_id)

    print("se pausa 10 min")
    print(hora())
    time.sleep(10*60) #this will stop the program for 10 minutes

    buscador()


buscador()
