import sys
import time
import requests
from pymongo import MongoClient
import os
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
            
    # ENTER PRISE data= {'chat_id': '-1001765171182','text': str(message) , 'parse_mode':ParseMode.HTML}  )
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



def brand_search(brand):
      

    t5 = collection5.find({"brand":{"$in":[ re.compile(brand, re.IGNORECASE)]}, "web_dsct":{"$gte":70}, "date": date})
    print( "se realizo busqueda")
    print(brand)
    for i in t5:
        print(i)
        print("se envio a telegram")      
        send_telegram ("<b>Marca: "+i["brand"]+"</b>\nModelo: "+i["product"]+"\nPrecio Lista :"+str(i["list_price"])+"\n<b>Precio web :"+str(i["best_price"])+"</b>\nPrecio Tarjeta :"+str(i["card_price"])+"\n"+i["image"]+"\n\nLink :"+i["link"])


def search_brand_dsct(brand,dsct):
      

    t5 = collection5.find({"brand":{"$in":[ re.compile(str(brand), re.IGNORECASE)]}, "web_dsct":{"$gte":int(dsct)}, "date": date})
    print( "se realizo busqueda")
    


    for i in t5:
        print(i)
        print("se envio a telegram")      
        send_telegram ("<b>Marca: "+i["brand"]+"</b>\nModelo: "+i["product"]+"\nPrecio Lista :"+str(i["list_price"])+"\n<b>Precio web :"+str(i["best_price"])+"</b>\nPrecio Tarjeta :"+str(i["card_price"])+"\n"+i["image"]+"\n\nLink :"+i["link"])
        time.sleep(1)

def product_search(producto,dsct):
      

    t5 = collection5.find({"product":{"$regex": re.compile(str(producto), re.IGNORECASE)}, "web_dsct":{"$gte":int(dsct)}, "date": date})
    print( "se realizo busqueda")
    


    for i in t5:
        print(i)
        print("se envio a telegram")      
        send_telegram ("<b>Marca: "+i["brand"]+"</b>\nModelo: "+i["product"]+"\nPrecio Lista :"+str(i["list_price"])+"\n<b>Precio web :"+str(i["best_price"])+"</b>\nPrecio Tarjeta :"+str(i["card_price"])+"\n"+i["image"]+"\n\nLink :"+i["link"])
        time.sleep(1)



def price_search(producto,price):
      

    t5 = collection5.find({"product":{"$regex": re.compile(str(producto), re.IGNORECASE)}, "list_price":{"$lte":price}, "date": date})
    t6 = collection5.find({"product":{"$regex": re.compile(str(producto), re.IGNORECASE)}, "best_price":{"$lte":price}, "date": date})
    t7 = collection5.find({"product":{"$regex": re.compile(str(producto), re.IGNORECASE)}, "card_price":{"$lte":price}, "date": date})


    print( "se realizo busqueda")
    
    pro = [t5,t6,t7]

    for idx, value in enumerate(pro):
        for i in value:
            print("se envia a telegram")
            send_telegram ("<b>Marca: "+i["brand"]+"</b>\nModelo: "+i["product"]+"\nPrecio Lista :"+str(i["list_price"])+"\n<b>Precio web :"+str(i["best_price"])+"</b>\nPrecio Tarjeta :"+str(i["card_price"])+"\n"+i["image"]+"\n\nLink :"+i["link"])
            time.sleep(1)

    # for i in pro:
    #     print(i)
    #     print("se envio a telegram")      
    #     send_telegram ("<b>Marca: "+i["brand"]+"</b>\nModelo: "+i["product"]+"\nPrecio Lista :"+str(i["list_price"])+"\n<b>Precio web :"+str(i["best_price"])+"</b>\nPrecio Tarjeta :"+str(i["card_price"])+"\n"+i["image"]+"\n\nLink :"+i["link"])
    #     time.sleep(1)







  
