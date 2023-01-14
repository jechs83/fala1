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



buscador()
