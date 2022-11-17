


import ast
import os
import re
import sys
import time
from datetime import datetime

import pymongo
import pytz
import requests
from bd_compare import save_data_to_mongo_db
from decouple import config
from pymongo import MongoClient
from telegram import ParseMode
server_date = datetime.now()
timezone = pytz.timezone("America/Bogota")
peru_date = server_date.astimezone(timezone)
date = peru_date.strftime("%d/%m/%Y" )

TOKEN = config("CAPITAN_PIKE_TOKEN")
chat_ide = config("EXCELSIOR_CHAT_TOKEN")
bot_tokey_key = config("CAPITAN_PIKE_TOKEN")


def send_telegram(message, bot_tokey_key, chat_ide):
    requests.post("https://api.telegram.org/bot"+str(bot_tokey_key)+"/sendMessage",
            
    data= {'chat_id': chat_ide ,'text': str(message) , 'parse_mode':ParseMode.HTML}  ) # DISC0VERY
    

client = MongoClient(config("MONGO_DB"))
db5 = client["scrap"]
collection5 = db5["scrap"] 
collection_offer1 = db5["excelsior1"]
collection_offer2 = db5["excelsior2"]


array_brand= ["sony", "lg", "panasonic"]

for brand in array_brand:

    t1 =  collection5.find( {"web_dsct":{ "$gte":70},"date":date ,"brand":{"$in":[ re.compile(str(brand),re.IGNORECASE) ]}})
    print(brand)

    for i in t1:

        send_telegram( ("<b>Marca: "+i["brand"]+"</b>\nModelo: "+i["product"]+"\nPrecio Lista :" +str(i["list_price"])+ "\n<b>Precio web :"+str(i["best_price"])+"</b>\nPrecio Tarjeta :"+str(i["card_price"])+"\n"+i["image"]+"\nLink :"+str(i["link"]))
                               ,bot_tokey_key, chat_ide)



