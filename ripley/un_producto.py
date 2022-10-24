import sys
import time
import requests
from pymongo import MongoClient
import os
import ast
import re
from datetime import datetime
from telegram import ParseMode
from g_var import mongo_db

date = datetime.today().strftime('%d-%m-%Y')
date_now = datetime.today().strftime('%d-%m-%Y')

mensaje = "test message"

def send_telegram(message):
    requests.post("https://api.telegram.org/bot5504401191:AAG8Wuk5AF95qEWn0642ZjhzduE0CbVkBaU/sendMessage",
            
   # ENTER PRISE data= {'chat_id': '-1001765171182','text': str(message) , 'parse_mode':ParseMode.HTML}  )
    data= {'chat_id': '-1001811194463','text': str(message) , 'parse_mode':ParseMode.HTML}  ) # DISC0VERY

client = MongoClient(mongo_db)

db = client["ripley"]
collection = db["market"] 

db2 = client["shopstar"]
collection2 = db2["market"] 

db3 = client["shopstar"]
collection3 = db3["promart"] 

db4 = client["cencosud"]
collection4 = db4["market"] 

db5 = client["scrap"]
collection5 = db5["scrap"] 

        

def busqueda(codigo):

## QUERYS DE MONGO PARA BUSCAR OFERTAS O PRECIOS BUGS 
    t1 = collection.find({"sku":codigo})
    t2 = collection2.find({"sku":codigo})
    t3 = collection3.find({"sku":codigo})
    try:
     t4 = collection4.find({"sku":int(codigo)})
    except: print("no hay wong")

    t5 = collection5.find({"sku":codigo})

    for i in t1:

       if not t1:
            print("no hay codigo")
    
       send_telegram ("<b>Marca: "+i["brand"]+"</b>\nModelo: "+i["product"]+"\nPrecio Lista :"+str(i["list_price"])+"\n<b>Precio web :"+str(i["best_price"])+"</b>\nPrecio Tarjeta :"+str(i["card_price"])+"\n"+i["image"]+"\n\nLink :"+i["link"])

    for i in t2:
        
      send_telegram ("<b>Marca: "+i["brand"]+"</b>\nModelo: "+i["product"]+"\nPrecio Lista :"+str(i["list_price"])+"\n<b>Precio web :"+str(i["best_price"])+"</b>\nPrecio Tarjeta :"+str(i["card_price"])+"\n"+i["image"]+"\n\nLink :"+i["link"])
 

    for i in t3:
        
     send_telegram ("<b>Marca: "+i["brand"]+"</b>\nModelo: "+i["product"]+"\nPrecio Lista :"+str(i["list_price"])+"\n<b>Precio web :"+str(i["best_price"])+"</b>\nPrecio Tarjeta :"+str(i["card_price"])+"\n"+i["image"]+"\n\nLink :"+i["link"])
    
    try:
        for i in t4:
              
          send_telegram ("<b>Marca: "+i["brand"]+"</b>\nModelo: "+i["product"]+"\nPrecio Lista :"+str(i["list_price"])+"\n<b>Precio web :"+str(i["best_price"])+"</b>\nPrecio Tarjeta :"+str(i["card_price"])+"\n"+i["image"]+"\n\nLink :"+i["link"])
    except: print("no hay wong")

    for i in t5:
            
     send_telegram ("<b>Marca: "+i["brand"]+"</b>\nModelo: "+i["product"]+"\nPrecio Lista :"+str(i["list_price"])+"\n<b>Precio web :"+str(i["best_price"])+"</b>\nPrecio Tarjeta :"+str(i["card_price"])+"\n"+i["image"]+"\n\nLink :"+i["link"])
    

  
