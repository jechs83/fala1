from datetime import datetime
from telegram import ParseMode
from decouple import config
import telegram
import logging
import sys
from telegram import message
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from search_bot_service import  auto_telegram



TOKEN = config("RICHI_BOY_TOKEN")
chat_id = config("RICHI_CHAT_TOKEN")
bot_token = config("RICHI_BOY_TOKEN")
bd1 = "richi1"
bd2 = "richi2"

auto_telegram("electro", bd1,bd2,bot_token, chat_id)

auto_telegram("tecno", bd1,bd2,bot_token, chat_id)

auto_telegram("juguetes", bd1,bd2,bot_token, chat_id)

auto_telegram("ropa", bd1,bd2,bot_token, chat_id)

auto_telegram("bicicleta", bd1,bd2,bot_token, chat_id)

auto_telegram("celular", bd1,bd2,bot_token, chat_id)

auto_telegram("herramientas", bd1,bd2,bot_token, chat_id)


