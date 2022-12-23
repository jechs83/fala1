import sys
import time
import requests
from pymongo import MongoClient
import os
import pymongo
import ast
import re
from decouple import config
from datetime import datetime
from telegram import ParseMode
import pytz
server_date = datetime.now()
timezone = pytz.timezone("America/Bogota")
peru_date = server_date.astimezone(timezone)
date = peru_date.strftime("%d/%m/%Y" )



def send_telegram(message):
    requests.post(config("TELEGRAM_KEY"),
            
    data= {'chat_id': '-1001811194463','text': str(message) , 'parse_mode':ParseMode.HTML}  ) # DISC0VERY
    

client = MongoClient(config("MONGO_DB"))
db5 = client["scrap"]
collection5 = db5["scrap"] 
  

def busqueda(codigo):
      

    t5 = collection5.find({"sku":str(codigo)})
    print( "se realizo busqueda")
    print(codigo)
    for i in t5:
        print(i)
        print("se envio a telegram")      
        send_telegram ("<b>Marca: "+i["brand"]+"</b>\nModelo: "+i["product"]+"\nPrecio Lista :"+str(i["list_price"])+"\n<b>Precio web :"+str(i["best_price"])+"</b>\nPrecio Tarjeta :"+str(i["card_price"])+"\n"+i["image"]+"\n\nLink :"+i["link"])




def search_brand_dsct(brand,dsct):
      
    if dsct <41:
        dsct = 40
    t5 = collection5.find({"brand":{"$in":[ re.compile(str(brand), re.IGNORECASE)]}, "web_dsct":{"$gte":int(dsct)}, "date": date}).sort([{"web_dsct", pymongo.DESCENDING}])
   
    print( "se realizo busqueda")

    count = 0
    for i in t5:
        count = count+1
        if count == 100:
            break
        print(i)
        print("se envio a telegram")      
        send_telegram ("<b>Marca: "+i["brand"]+"</b>\nModelo: "+i["product"]+"\nPrecio Lista :"+str(i["list_price"])+"\n<b>Precio web :"+str(i["best_price"])+"</b>\nPrecio Tarjeta :"+str(i["card_price"])+"\n"+i["image"]+"\n\nLink :"+i["link"])
        time.sleep(1)







