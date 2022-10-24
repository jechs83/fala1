from enum import auto
import sys
import time
import requests
from pymongo import MongoClient
import os
import ast
from g_var import mongo_db
import re
from datetime import datetime
from telegram import ParseMode


date = datetime.today().strftime('%d/%m/%Y')
date_now = datetime.today().strftime('%d/%m/%Y')
print(date_now)

mensaje = "test message"

def send_telegram(message):
    requests.post("https://api.telegram.org/bot5504401191:AAG8Wuk5AF95qEWn0642ZjhzduE0CbVkBaU/sendMessage",
            
   # ENTER PRISE data= {'chat_id': '-1001765171182','text': str(message) , 'parse_mode':ParseMode.HTML}  )
    data= {'chat_id': '-1001811194463','text': str(message) , 'parse_mode':ParseMode.HTML}  ) # DISC0VERY

client = MongoClient(mongo_db)

        
db = client["scrap"]
collection = db["scrap"] 

## QUERYS DE MONGO PARA BUSCAR OFERTAS O PRECIOS BUGS 
t1 =  collection.find( {"web_dsct":{"$gte":80},"date":date_now,"brand":{"$in":[ 
    re.compile("samsung", re.IGNORECASE),re.compile("lenovo", re.IGNORECASE),re.compile("sony", re.IGNORECASE),
    re.compile("lg", re.IGNORECASE),re.compile("asus", re.IGNORECASE),re.compile("xiaomi", re.IGNORECASE),
    re.compile("indurama", re.IGNORECASE),re.compile("oster", re.IGNORECASE),re.compile("bosch", re.IGNORECASE),
    re.compile("acer", re.IGNORECASE),re.compile("huawei", re.IGNORECASE),re.compile("panasonic", re.IGNORECASE),
    re.compile("winia", re.IGNORECASE),re.compile("phillips", re.IGNORECASE),re.compile("mabe", re.IGNORECASE),
    re.compile("nex", re.IGNORECASE) 
    
                                   
     ]}})

#t2 =  collection.find( { "date" : date_now, "web_dsct" : { "$gte" : 90} } )
print(t1)

pro = [t1]  ## ARREGLO DE LOS QUERYS DE MONGO PARA MANDAR POR TELEGRAM
products = []

## FUNCION QUE COLOCA EN UNA LISTA (products) TODO LOS PRODUCTOS PARA SER MANDADOS A TELEGRAM,
## AQUI SE LE PASA EL OBJETO  MONGO PARA ITERACION Y EXTRACCIONDE LOS CAMPOS
def mongodb_search():
    for idx, value in enumerate(pro):
        for i in value:
            print(i)
            mongo_obj = [   i["image"], i["brand"] , i["product"], i["list_price"], 
                            i["best_price"], i["card_price"], i["link"] ,i["web_dsct"],i["sku"]
                        ]
            #print(val)
            products.append(mongo_obj)
            time.sleep(2)
    print(products)


def auto_telegram():
    mongodb_search()
    for i,v in enumerate(products):
       send_telegram ("<b>Marca: "+v[1]+"</b>\nModelo: "+v[2]+"\nPrecio Lista :"+str(v[3])+"\n<b>Precio web :"+str(v[4])+"</b>\nPrecio Tarjeta :"+str(v[5])+"\n"+v[0]+"\nLink :"+str(v[6]))
    
auto_telegram()


