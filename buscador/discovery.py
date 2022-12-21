from datetime import datetime
from telegram import ParseMode
from decouple import config
import telegram
import logging
import sys
from telegram import message
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from bot_unique import super_bot




TOKEN = config("CAPITAN_SPOK_TOKEN")
chat_ide = config("DISCOVERY_CHAT_TOKEN")
bot_token = config("CAPITAN_SPOK_TOKEN")


super_bot(TOKEN,chat_ide, bot_token)

