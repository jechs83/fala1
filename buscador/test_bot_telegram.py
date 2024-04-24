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


import requests


def send_telegram(message, foto, bot_token, chat_id):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
            'Referer': 'https://home.ripley.com.pe'
        }
        response = requests.get(foto, headers=headers)
        response.raise_for_status()
        photo_data = response.content
        
        # Send photo using Telegram API
        telegram_response = requests.post(
            f'https://api.telegram.org/bot{bot_token}/sendPhoto',
            data={'chat_id': chat_id, 'caption': str(message), "parse_mode": "HTML"},
            files={'photo': photo_data},
        )
        
        telegram_response.raise_for_status()
        print("Message sent successfully via the Telegram function.")
    except requests.exceptions.RequestException as e:
        print("Error occurred during the request:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)

# Example usage
foto = "https://home.ripley.com.pe/Attachment/WOP_5/2032313979740/2032313979740_2.jpg"
chat_id = config("OH2")

bot_token = config("LLAMA_6_BOT")
message = prueba"

send_telegram(message, foto, bot_token, chat_id)



