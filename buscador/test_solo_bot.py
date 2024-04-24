import sys
import time
from html_test import html_code
import gc
from pymongo import MongoClient
import itertools
import re
import base64
import requests



import pymongo
from bd_compare import save_data_to_mongo_db
from history_price import compare_prices

from decouple import config
from datetime import datetime
import telegram
from pandas import DataFrame
import pytz
from datetime import datetime

server_date = datetime.now()
timezone = pytz.timezone("America/Bogota")
peru_date = server_date.astimezone(timezone)

from pymongo import MongoClient
from decouple import config
client = MongoClient(config("MONGO_DB"))
#date = peru_date.strftime("%d/%m/%Y" )
#oferta_telegram = "👉 https://t.me/OfertasDescuentosPeru1 👈"
oferta_telegram = ""

#https://api.telegram.org/bot5573005249:AAFGCjc7zuI1XoHMqbd6gr1I1ZVi9Xd2I9s/sendMessage


def dia():
    now = datetime.now()
    date = now.strftime("%d/%m/%Y")
    #date = date.today()
    return date

date = dia()


def send_telegram(message,foto, bot_token, chat_id):

    # if not foto:
    #     foto="https://image.shutterstock.com/image-vector/no-image-available-sign-absence-260nw-373243873.jpg"
    
    # if len(foto)<=4:
    #         foto="https://image.shutterstock.com/image-vector/no-image-available-sign-absence-260nw-373243873.jpg"

    print(foto)
    response = requests.post(
        
        f'https://api.telegram.org/bot{bot_token}/sendPhoto',
        data={'chat_id': chat_id, 'caption': str(message), "parse_mode": "HTML"},
        files={'photo': requests.get(foto).content},
    
        )
    print("se envio mensaje por funcion de telegram")


msn = ( "prueba" )

foto = "https://home.ripley.com.pe/Attachment/WOP_5/2032313979740/2032313979740_2.jpg"


chat_id = config("OH2")

bot_token = config("LLAMA_6_BOT")
send_telegram (msn,foto, bot_token, chat_id)


