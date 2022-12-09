import sys
import time
import requests
from pymongo import MongoClient
import os
import pymongo
import re
from bd_compare import save_data_to_mongo_db
from decouple import config
from datetime import datetime
from telegram import ParseMode
import pytz
from pandas import DataFrame
import pandas as pd

server_date = datetime.now()
timezone = pytz.timezone("America/Bogota")
peru_date = server_date.astimezone(timezone)
date = peru_date.strftime("%d/%m/%Y" )

chat_ide = config("EXCELSIOR_CHAT_TOKEN")
bot_token = config("CAPITAN_PIKE_TOKEN")

#https://api.telegram.org/bot5573005249:AAFGCjc7zuI1XoHMqbd6gr1I1ZVi9Xd2I9s/sendMessage

def send_telegram(message, bot_token, chat_ide):
    requests.post("https://api.telegram.org/bot"+str(bot_token)+"/sendMessage",
            
    data= {'chat_id': chat_ide ,'text': str(message) , 'parse_mode':ParseMode.HTML}  ) # DISC0VERY
    

client = MongoClient(config("MONGO_DB"))
db5 = client["scrap"]
collection5 = db5["scrap"]  



def search_market_dsct(market,dsct, bot_tokey_key, chat_ide):
  
    if dsct <41:
        dsct = 40
    t5 = collection5.find({"market":market, "web_dsct":{"$gte":int(dsct)}, "brand":{"$nin":[re.compile("generica", re.IGNORECASE), re.compile("generico", re.IGNORECASE),  re.compile("genérico", re.IGNORECASE), re.compile("genérica", re.IGNORECASE),  re.compile("generic", re.IGNORECASE)] }, "date": date})

    list_cur = list(t5)
    products = []
    for i in list_cur:
        
        market = i["market"]
        p = {"market": i["market"],"brand": i["brand"], "product": i["product"], 'list_price': i["list_price"], 'best_price': i["best_price"], 'card_price': i["card_price"], 'web_dsct': i["web_dsct"], 'card_dsct': i["card_dsct"], 'link':  '<a href='+i["link"]+'>Link</a>' , 'image': '<img src='+i["image"]+" style=max-height:124px;/>", 'date': i["date"], 'time':i["time"]}
        products.append(p)

    df = DataFrame(products)
    
    def path_to_image_html(path):
 
        return '<img src="'+ path + '" style=max-height:124px;"/>'

    html = df.to_html(escape=False ,formatters=dict(column_name_with_image_links=path_to_image_html))

    with open ("/Users/javier/GIT/fala/buscador/web.html", "w") as f:
        f.write(html)
        f.close
    print(html)
    send_telegram(html, bot_token, chat_ide )

    # print( "se realizo busqueda")

    # count = 0
    # for i in t5:
    #     count = count+1
    #     if count == 100:
    #         break
    #     print(i)
    #     print("se envio a telegram")   
    #     msn =  "<b>Marca: "+i["brand"]+"</b>\nModelo: "+i["product"]+"\nPrecio Lista :"+str(i["list_price"])+"\n<b>Precio web :"+str(i["best_price"])+"</b>\nPrecio Tarjeta :"+str(i["card_price"])+"\n"+i["image"]+"\n\nLink :"+i["link"]

    #     send_telegram (msn, bot_tokey_key, chat_ide)
    #     time.sleep(2)
