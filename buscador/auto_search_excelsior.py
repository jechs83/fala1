from datetime import datetime
from telegram import ParseMode
from decouple import config
import telegram
import logging
import sys
import time
from telegram import message
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from search_bot_service import  auto_telegram ,auto_telegram_total



TOKEN = config("CAPITAN_PIKE_TOKEN")
chat_id = config("EXCELSIOR_CHAT_TOKEN")
bot_token = config("CAPITAN_PIKE_TOKEN")
bd1 = "excelsior1"
bd2 = "excelsior2"
porcentage = 70

def hora():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

def buscador():
    auto_telegram_total( bd1,bd2,bot_token, chat_id, porcentage)


    print("se pausa 10 min")
    print(hora())
    time.sleep(60) #this will stop the program for 10 minutes

    buscador()


buscador()
