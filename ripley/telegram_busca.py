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



def send_telegram(message):
    requests.post("https://api.telegram.org/bot5504401191:AAG8Wuk5AF95qEWn0642ZjhzduE0CbVkBaU/sendMessage",
            
    # ENTER PRISE data= {'chat_id': '-1001765171182','text': str(message) , 'parse_mode':ParseMode.HTML}  )
    data= {'chat_id': '-1001811194463','text': str(message) , 'parse_mode':ParseMode.HTML}  ) # DISC0VERY
    

client = MongoClient(mongo_db)

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





  
