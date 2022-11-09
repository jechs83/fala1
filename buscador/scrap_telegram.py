from enum import auto
import sys
import time
import requests
from pymongo import MongoClient
import os
import ast
import re

from datetime import datetime
from telegram import ParseMode
from decouple import config


date = datetime.today().strftime('%d/%m/%Y')
date_now = datetime.today().strftime('%d/%m/%Y')
print(date_now)

mensaje = "test message"

def send_telegram(message):
    requests.post(config("TELEGRAM_KEY"),
            
    # ENTER PRISE data= {'chat_id': '-1001765171182','text': str(message) , 'parse_mode':ParseMode.HTML}  )
    data= {'chat_id': '-1001811194463','text': str(message) , 'parse_mode':ParseMode.HTML}  ) # DISC0VERY


client = MongoClient(config("MONGO_DB"))

        
db = client["scrap"]
collection = db["scrap"] 

## QUERYS DE MONGO PARA BUSCAR OFERTAS O PRECIOS BUGS 
t1 =  collection.find( {"web_dsct":{ "$gte":70},"date":date_now ,"brand":{"$in":[ 
    re.compile("samsung", re.IGNORECASE),re.compile("lenovo", re.IGNORECASE),re.compile("sony", re.IGNORECASE),
    re.compile("lg", re.IGNORECASE),re.compile("asus", re.IGNORECASE),re.compile("xiaomi", re.IGNORECASE),
    re.compile("indurama", re.IGNORECASE),re.compile("oster", re.IGNORECASE),re.compile("bosch", re.IGNORECASE),
    re.compile("acer", re.IGNORECASE),re.compile("huawei", re.IGNORECASE),re.compile("panasonic", re.IGNORECASE),
    re.compile("winia", re.IGNORECASE),re.compile("phillips", re.IGNORECASE),re.compile("mabe", re.IGNORECASE),
    re.compile("nex", re.IGNORECASE), re.compile("hyundai", re.IGNORECASE),re.compile("tcl", re.IGNORECASE), re.compile("monark", re.IGNORECASE), 
    re.compile("goliat", re.IGNORECASE), re.compile("oxford", re.IGNORECASE), re.compile("jafi-bike", re.IGNORECASE), re.compile("besatti", re.IGNORECASE), 
    re.compile("altitude", re.IGNORECASE), re.compile("trek", re.IGNORECASE), re.compile("advantech", re.IGNORECASE), re.compile("ecoride", re.IGNORECASE),
    re.compile("izytek", re.IGNORECASE),re.compile("movimiento", re.IGNORECASE),re.compile("xclusive", re.IGNORECASE),re.compile("cross", re.IGNORECASE),
    re.compile("jvc", re.IGNORECASE),re.compile("motorola", re.IGNORECASE),re.compile("bgh", re.IGNORECASE),re.compile("hisense", re.IGNORECASE),
    re.compile("blackline", re.IGNORECASE),re.compile("daewoo", re.IGNORECASE),re.compile("dell", re.IGNORECASE),
    re.compile("hp", re.IGNORECASE),re.compile("honor", re.IGNORECASE),re.compile("advance", re.IGNORECASE),
    re.compile("gigabyte", re.IGNORECASE),re.compile("msi", re.IGNORECASE),re.compile("vastec", re.IGNORECASE),
    re.compile("xpg", re.IGNORECASE),re.compile("alienware", re.IGNORECASE),re.compile("SENNHEISER", re.IGNORECASE),
    re.compile("HIKVISION", re.IGNORECASE),re.compile("logitech", re.IGNORECASE),re.compile("EZVIZ", re.IGNORECASE),
    re.compile("BEHRINGER", re.IGNORECASE),re.compile("google", re.IGNORECASE),re.compile("dji", re.IGNORECASE),
    re.compile("best", re.IGNORECASE),re.compile("amazon", re.IGNORECASE),re.compile("sonos", re.IGNORECASE),
    re.compile("TP LINK", re.IGNORECASE),re.compile("razer", re.IGNORECASE),re.compile("UMIDIGI", re.IGNORECASE),
    re.compile("vivo", re.IGNORECASE),re.compile("oppo", re.IGNORECASE),re.compile("kingston", re.IGNORECASE),
    re.compile("sonoff", re.IGNORECASE),re.compile("makita", re.IGNORECASE),re.compile("thomas", re.IGNORECASE),
    re.compile("baseus", re.IGNORECASE),re.compile("karcher", re.IGNORECASE),re.compile("stanley", re.IGNORECASE),
    re.compile("BLACK AND DECKER", re.IGNORECASE),re.compile("BLACK & DECKER", re.IGNORECASE),re.compile("dewalt", re.IGNORECASE),
    re.compile("skil", re.IGNORECASE),re.compile("bauker", re.IGNORECASE),re.compile("uberman", re.IGNORECASE),
    re.compile("fujifilm", re.IGNORECASE),re.compile("nikon", re.IGNORECASE),re.compile("aiwa", re.IGNORECASE),
    re.compile("microsoft", re.IGNORECASE),re.compile("tp-link", re.IGNORECASE),re.compile("fuji", re.IGNORECASE),
    re.compile("ADIDAS", re.IGNORECASE),re.compile("ASICS", re.IGNORECASE),re.compile("NEW BALANCE", re.IGNORECASE),
    re.compile("nike", re.IGNORECASE),re.compile("puma", re.IGNORECASE),re.compile("reebok", re.IGNORECASE),
    re.compile("skechers", re.IGNORECASE),re.compile("under armour", re.IGNORECASE),re.compile("umbro", re.IGNORECASE),
    re.compile("Clementoni", re.IGNORECASE),re.compile("vainsa", re.IGNORECASE),re.compile("ibm", re.IGNORECASE),
    re.compile("lego", re.IGNORECASE),re.compile("intel", re.IGNORECASE),re.compile("louis vuitton", re.IGNORECASE),
    re.compile("prada", re.IGNORECASE),re.compile("gucc8i", re.IGNORECASE),re.compile("pampers", re.IGNORECASE),
    re.compile("zara", re.IGNORECASE),re.compile("canon", re.IGNORECASE),re.compile("caterpillar", re.IGNORECASE),
    re.compile("nintendo", re.IGNORECASE),re.compile("rolex", re.IGNORECASE),re.compile("nokia", re.IGNORECASE),
    re.compile("lexus", re.IGNORECASE),re.compile("exxon mobil", re.IGNORECASE),re.compile("ralph lauren", re.IGNORECASE),
    re.compile("apple", re.IGNORECASE),re.compile("chicco", re.IGNORECASE),re.compile("safety", re.IGNORECASE),
    re.compile("cosco", re.IGNORECASE),re.compile("infanti", re.IGNORECASE),re.compile("invicta22", re.IGNORECASE),
    re.compile("fisher price", re.IGNORECASE),re.compile("Hot wheels", re.IGNORECASE),re.compile("cry babies", re.IGNORECASE),
    re.compile("my little pony", re.IGNORECASE),re.compile("Baby alive", re.IGNORECASE),re.compile("index", re.IGNORECASE),
    re.compile("barbie", re.IGNORECASE)
    
    
                                   
     ]}})

#t2 =  collection.find( { "date" : date_now, "web_dsct" : { "$gte" : 90} } )

pro = [t1]  ## ARREGLO DE LOS QUERYS DE MONGO PARA MANDAR POR TELEGRAM
products = []

## FUNCION QUE COLOCA EN UNA LISTA (products) TODO LOS PRODUCTOS PARA SER MANDADOS A TELEGRAM,
## AQUI SE LE PASA EL OBJETO  MONGO PARA ITERACION Y EXTRACCIONDE LOS CAMPOS
def mongodb_search():
    for idx, value in enumerate(pro):
        for i in value:
            mongo_obj = [   i["image"], i["brand"] , i["product"], i["list_price"], 
                            i["best_price"], i["card_price"], i["link"] ,i["web_dsct"],i["sku"]
                        ]
            #print(val)
            products.append(mongo_obj)
            print()
            print(i["sku"])
            print(i["brand"])
            print(i["product"])
            print(i["link"])
            send_telegram( ("<b>Marca: "+i["brand"]+"</b>\nModelo: "+i["product"]+"\nPrecio Lista :"+str(i["list_price"])+"\n<b>Precio web :"+str(i["best_price"])+"</b>\nPrecio Tarjeta :"+str(i["card_price"])+"\n"+i["image"]+"\nLink :"+str(i["link"])))
            time.sleep(1)
    


def auto_telegram():
    mongodb_search()
    #for i,v in enumerate(products):
     #  send_telegram ("<b>Marca: "+v[1]+"</b>\nModelo: "+v[2]+"\nPrecio Lista :"+str(v[3])+"\n<b>Precio web :"+str(v[4])+"</b>\nPrecio Tarjeta :"+str(v[5])+"\n"+v[0]+"\nLink :"+str(v[6]))
    
auto_telegram()


