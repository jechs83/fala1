import sys
import time
import requests
from pymongo import MongoClient
import os
import pymongo
import ast
import re
from bd_compare import save_data_to_mongo_db
from decouple import config
from datetime import datetime
from telegram import ParseMode
import pytz
server_date = datetime.now()
timezone = pytz.timezone("America/Bogota")
peru_date = server_date.astimezone(timezone)
date = peru_date.strftime("%d/%m/%Y" )

TOKEN = config("CAPITAN_SPOK_TOKEN")
chat_ide = config("DISCOVERY_CHAT_TOKEN")
bot_token = config("CAPITAN_SPOK_TOKEN")


def send_telegram(message, bot_tokey_key, chat_ide):
    requests.post("https://api.telegram.org/bot"+str(bot_tokey_key)+"/sendMessage",
            
    data= {'chat_id': chat_ide ,'text': str(message) , 'parse_mode':ParseMode.HTML}  ) 
    

client = MongoClient(config("MONGO_DB"))
db5 = client["scrap"]
collection5 = db5["scrap"] 
collection_offer1 = db5["enterprise1"]
collection_offer2 = db5["enterprise2"]


t1 =  collection5.find( {"web_dsct":{ "$gte":70},"date":date ,"brand":{"$in":[ 
re.compile("samsung", re.IGNORECASE),re.compile("lenovo", re.IGNORECASE),re.compile("Lg", re.IGNORECASE),re.compile("Asus", re.IGNORECASE),re.compile("Xiaomi", re.IGNORECASE),re.compile("indurama", re.IGNORECASE),re.compile("oster", re.IGNORECASE),re.compile("bosch", re.IGNORECASE),re.compile("acer", re.IGNORECASE),re.compile("huawei", re.IGNORECASE),re.compile("panasonic", re.IGNORECASE),re.compile("winnia", re.IGNORECASE),re.compile("phillips", re.IGNORECASE),re.compile("mabe", re.IGNORECASE),re.compile("nex", re.IGNORECASE),re.compile("hyundai", re.IGNORECASE),re.compile("tcl", re.IGNORECASE),re.compile("monark ", re.IGNORECASE),re.compile("goliat ", re.IGNORECASE),re.compile("oxford ", re.IGNORECASE),re.compile("jafi-bike ", re.IGNORECASE),re.compile("besatti ", re.IGNORECASE),re.compile("altitude ", re.IGNORECASE),re.compile("trek ", re.IGNORECASE),re.compile("advantech ", re.IGNORECASE),re.compile("ecoride", re.IGNORECASE),re.compile("izytek", re.IGNORECASE),re.compile("movimiento", re.IGNORECASE),re.compile("xclusive", re.IGNORECASE),re.compile("cross", re.IGNORECASE),re.compile("jvc", re.IGNORECASE),re.compile("motorola", re.IGNORECASE),re.compile("bgh", re.IGNORECASE),re.compile("hisense", re.IGNORECASE),re.compile("blackline", re.IGNORECASE),re.compile("daewoo", re.IGNORECASE),re.compile("dell", re.IGNORECASE),re.compile("hp", re.IGNORECASE),re.compile("honor", re.IGNORECASE),re.compile("advance", re.IGNORECASE),re.compile("gigabyte", re.IGNORECASE),re.compile("msi", re.IGNORECASE),re.compile("vastec", re.IGNORECASE),re.compile("xpg", re.IGNORECASE),re.compile("alienware", re.IGNORECASE),re.compile("SENNHEISER", re.IGNORECASE),re.compile("HIKVISION", re.IGNORECASE),re.compile("logitech", re.IGNORECASE),re.compile("EZVIZ", re.IGNORECASE),re.compile("BEHRINGER", re.IGNORECASE),re.compile("googledji", re.IGNORECASE),re.compile("best", re.IGNORECASE),re.compile("amazon", re.IGNORECASE),re.compile("sonos", re.IGNORECASE),re.compile("TP LINK", re.IGNORECASE),re.compile("razer", re.IGNORECASE),re.compile("UMIDIGI", re.IGNORECASE),re.compile("vivo", re.IGNORECASE),re.compile("oppo", re.IGNORECASE),re.compile("kingston", re.IGNORECASE),re.compile("sonoff", re.IGNORECASE),re.compile("makita", re.IGNORECASE),re.compile("thomas", re.IGNORECASE),re.compile("baseus", re.IGNORECASE),re.compile("karcher", re.IGNORECASE),re.compile("stanley", re.IGNORECASE),re.compile("BLACK AND DECKER", re.IGNORECASE),re.compile("BLACK & DECKER", re.IGNORECASE),re.compile("dewalt", re.IGNORECASE),re.compile("skil", re.IGNORECASE),re.compile("bauker", re.IGNORECASE),re.compile("uberman", re.IGNORECASE),re.compile("fujifilm", re.IGNORECASE),re.compile("nikonaiwa", re.IGNORECASE),re.compile("microsoft", re.IGNORECASE),re.compile("tp-link", re.IGNORECASE),re.compile("fuji", re.IGNORECASE),re.compile("ADIDAS", re.IGNORECASE),re.compile("ASICS", re.IGNORECASE),re.compile("NEW BALANCE", re.IGNORECASE),re.compile("nike", re.IGNORECASE),re.compile("puma", re.IGNORECASE),re.compile("reebok", re.IGNORECASE),re.compile("skechers", re.IGNORECASE),re.compile("under armour", re.IGNORECASE),re.compile("umbro", re.IGNORECASE),re.compile("Clementoni", re.IGNORECASE),re.compile("vainsa", re.IGNORECASE),re.compile("ibm", re.IGNORECASE),re.compile("lego", re.IGNORECASE),re.compile("intel", re.IGNORECASE),re.compile("louis vuitton", re.IGNORECASE),re.compile("prada", re.IGNORECASE),re.compile("pampers", re.IGNORECASE),re.compile("zara", re.IGNORECASE),re.compile("canon", re.IGNORECASE),re.compile("caterpillar", re.IGNORECASE),re.compile("nintendo", re.IGNORECASE),re.compile("rolex", re.IGNORECASE),re.compile("nokia", re.IGNORECASE),re.compile("lexus", re.IGNORECASE),re.compile("exxon mobil", re.IGNORECASE),re.compile("ralph lauren", re.IGNORECASE),re.compile("apple", re.IGNORECASE),re.compile("chicco", re.IGNORECASE),re.compile("safety", re.IGNORECASE),re.compile("cosco", re.IGNORECASE),re.compile("infanti", re.IGNORECASE),re.compile("fisher price", re.IGNORECASE),re.compile("Hot wheels", re.IGNORECASE),re.compile("cry babies", re.IGNORECASE),re.compile("my little pony", re.IGNORECASE),re.compile("Baby alive", re.IGNORECASE),re.compile("index", re.IGNORECASE),re.compile("barbie", re.IGNORECASE),re.compile("Avent", re.IGNORECASE),re.compile("Baby Club Chic", re.IGNORECASE),re.compile("Baby Harvest", re.IGNORECASE),re.compile("Baby liss", re.IGNORECASE),re.compile("Babycottons", re.IGNORECASE),re.compile("Barbados", re.IGNORECASE),re.compile("basemet", re.IGNORECASE),re.compile("Bata", re.IGNORECASE),re.compile("Bblubs", re.IGNORECASE),re.compile("Blackout", re.IGNORECASE),re.compile("BORN", re.IGNORECASE),re.compile("Bosse", re.IGNORECASE),re.compile("Bronco", re.IGNORECASE),re.compile("Bubble gummers", re.IGNORECASE),re.compile("cacharel", re.IGNORECASE),re.compile("Carters", re.IGNORECASE),re.compile("caterpilla", re.IGNORECASE),re.compile("Champion", re.IGNORECASE),re.compile("Cloudbreak", re.IGNORECASE),re.compile("Colloky", re.IGNORECASE),re.compile("columbia", re.IGNORECASE),re.compile("crocs", re.IGNORECASE),re.compile("diadora", re.IGNORECASE),re.compile("Diesel", re.IGNORECASE),re.compile("DJI", re.IGNORECASE),re.compile("Drimer", re.IGNORECASE),re.compile("Drom", re.IGNORECASE),re.compile("Dunkelvolk", re.IGNORECASE),re.compile("Edufun", re.IGNORECASE),re.compile("Emma Cotton Babies", re.IGNORECASE),re.compile("Evenflo", re.IGNORECASE),re.compile("Forli", re.IGNORECASE),re.compile("Gama", re.IGNORECASE),re.compile("Gotcha", re.IGNORECASE),re.compile("Gymboree", re.IGNORECASE),re.compile("Huggies", re.IGNORECASE),re.compile("Hugo boss", re.IGNORECASE),re.compile("Jack & Jones", re.IGNORECASE),re.compile("Kansas", re.IGNORECASE),re.compile("Kayra Man", re.IGNORECASE),re.compile("lacoste", re.IGNORECASE),re.compile("Lee", re.IGNORECASE),re.compile("Levis", re.IGNORECASE),re.compile("Little mommy", re.IGNORECASE),re.compile("Little tikes", re.IGNORECASE),re.compile("Lois", re.IGNORECASE),re.compile("lotto", re.IGNORECASE),re.compile("marquis", re.IGNORECASE),re.compile("Maui and Sons", re.IGNORECASE),re.compile("merrell", re.IGNORECASE),re.compile("Mountain gear", re.IGNORECASE),re.compile("NBA", re.IGNORECASE),re.compile("New Era", re.IGNORECASE),re.compile("Next", re.IGNORECASE),re.compile("Ninebot", re.IGNORECASE),re.compile("north face", re.IGNORECASE),re.compile("North star", re.IGNORECASE),re.compile("Oakley", re.IGNORECASE),re.compile("Osh kosh", re.IGNORECASE),re.compile("Parada 111", re.IGNORECASE),re.compile("Paraiso", re.IGNORECASE),re.compile("Pionier", re.IGNORECASE),re.compile("Quiksilver", re.IGNORECASE),re.compile("Reef", re.IGNORECASE),re.compile("Robert Lewis", re.IGNORECASE),re.compile("rusty", re.IGNORECASE),re.compile("Scoop", re.IGNORECASE),re.compile("Siegen", re.IGNORECASE),re.compile("Sybilla", re.IGNORECASE),re.compile("Tap out", re.IGNORECASE),re.compile("Volcom", re.IGNORECASE),re.compile("Wahl", re.IGNORECASE),re.compile("Whirpool", re.IGNORECASE),re.compile("Woallance", re.IGNORECASE),    
    ]}})

pro = [t1]  ## ARREGLO DE LOS QUERYS DE MONGO PARA MANDAR POR TELEGRAM
products = []

## FUNCION QUE COLOCA EN UNA LISTA (products) TODO LOS PRODUCTOS PARA SER MANDADOS A TELEGRAM,
## AQUI SE LE PASA EL OBJETO  MONGO PARA ITERACION Y EXTRACCIONDE LOS CAMPOS
def auto_telegram():
    db_name = "scrap"
    db_collection1 = "enterprise1"
    db_collection2 = "enterprise2"
    for idx, value in enumerate(pro):

        for i in value:

            save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                            i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],db_collection1)
  

            a= collection_offer1.find({"sku":i["sku"]})
            # se busca datos en offer1 cada iteracion
            a=list(a)
            b= collection_offer2.find({"sku":i["sku"]})
            # se busca datos en offer2  en cada iteracion 
            b = list(b)
            print(b)
            len_b = len(b)
            print(len_b)
            if len_b == 0:
                save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                            i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],db_collection2)
                send_telegram( ("<b>Marca: "+i["brand"]+"</b>\nModelo: "+i["product"]+"\nPrecio Lista :" +str(i["list_price"])+ "\n<b>Precio web :"+str(i["best_price"])+"</b>\nPrecio Tarjeta :"+str(i["card_price"])+"\n"+i["image"]+"\nLink :"+str(i["link"]))
                                ,bot_tokey_key, chat_ide )

                print(" b no extiste")
                continue

            if b!=a:
                send_telegram( ("<b>Marca: "+i["brand"]+"</b>\nModelo: "+i["product"]+"\nPrecio Lista :" +str(i["list_price"])+ "\n<b>Precio web :"+str(i["best_price"])+"</b>\nPrecio Tarjeta :"+str(i["card_price"])+"\n"+i["image"]+"\nLink :"+str(i["link"])), bot_tokey_key,  chat_ide, )
                print("SON DIFERENTES SE MANDA MENSAJE")
                save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                            i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],db_collection2)
                continue
            if a==b:
                print("son iguales no se envia nada")
                save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                            i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],db_collection2)

    #send_telegram( ("No se encontro nada mas en la bsuqueda automatica mayor igual a  70%"))
auto_telegram()