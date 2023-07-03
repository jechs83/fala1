from datetime import datetime
from telegram import ParseMode
from decouple import config
import telegram
import logging
import sys
from telegram import message
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from search_bot_service import busqueda, search_brand_dsct, auto_telegram, delete_brand,add_brand_list,read_brands,manual_telegram, search_market_dsct,search_market2_dsct, search_product_dsct_html


from bot_unique_deep import super_bot



TOKEN = config("CAPITAN_PIKE_TOKEN")
chat_id = config("DEEP_CHAT_TOKEN")
bot_token = config("CAPITAN_PIKE_TOKEN")


db1 = "deep1"
db2 = "deep2"
super_bot(TOKEN, bot_token, chat_id, db1, db2)

