from datetime import datetime
from telegram import ParseMode
from decouple import config
import telegram
import logging
import sys
from telegram import message
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from search_bot_service import  auto_telegram, auto_telegram_total
import time


now = datetime.now()
current_time = now.strftime("%H:%M:%S")

TOKEN = config("RICHI_BOY_TOKEN")
chat_id = config("RICHI_CHAT_TOKEN")
bot_token = config("RICHI_BOY_TOKEN")
bd1 = "richi1"
bd2 = "richi2"
porcentage = 50

def hora():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

def buscador_richi():
    auto_telegram_total( bd1,bd2,bot_token, chat_id, porcentage)


    print("se pausa 60 seg")
    print(hora())
    time.sleep(60) #this will stop the program for 10 minutes
    

             
i = 1                                         

def richi ():

    while i == 1:
        try:
            buscador_richi()
       
        except:
            richi()
richi()

