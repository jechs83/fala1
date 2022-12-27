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

TOKEN = config("CAPITAN_JANEWAY_TOKEN")
chat_ide = config("VOYAGER_CHAT_TOKEN")
bot_tokey_key = config("CAPITAN_JANEWAY_TOKEN")


def send_telegram(message, bot_tokey_key, chat_ide):
    requests.post("https://api.telegram.org/bot"+str(bot_tokey_key)+"/sendMessage",
            
    data= {'chat_id': chat_ide ,'text': str(message) , 'parse_mode':ParseMode.HTML}  ) # DISC0VERY
    

client = MongoClient(config("MONGO_DB"))
db5 = client["scrap"]
collection5 = db5["scrap"] 
collection_offer1 = db5["voyager1"]
collection_offer2 = db5["voyager2"]








t1 =  collection5.find( {"web_dsct":{ "$gte":70},"date":date ,"brand":{"$in":[ 

re.compile("Basement",re.IGNORECASE), re.compile("Bearcliff",re.IGNORECASE), re.compile("Calvin Klein",re.IGNORECASE), re.compile("Casio",re.IGNORECASE), re.compile("Christian Lacroix",re.IGNORECASE), re.compile("Denimlab",re.IGNORECASE), re.compile("Dockers",re.IGNORECASE), re.compile("Doo Australia",re.IGNORECASE), re.compile("Guess",re.IGNORECASE), re.compile("La Martina",re.IGNORECASE), re.compile("Mango",re.IGNORECASE), re.compile("Mossimo",re.IGNORECASE), re.compile("Newport",re.IGNORECASE), re.compile("Polo Ralph Lauren",re.IGNORECASE), re.compile("Ray Ban",re.IGNORECASE), re.compile("Riff&Raff",re.IGNORECASE), re.compile("Springfield",re.IGNORECASE), re.compile("Superdry",re.IGNORECASE), re.compile("Tommy Hilfiger",re.IGNORECASE), re.compile("University Club",re.IGNORECASE), re.compile("Wolf&Hank",re.IGNORECASE), re.compile("HARVEST",re.IGNORECASE), re.compile("CLARINS",re.IGNORECASE), re.compile("NAVIGATA",re.IGNORECASE), re.compile("CLOUDBREAK",re.IGNORECASE), re.compile("KENNETH STEVENS",re.IGNORECASE), re.compile("STRAWBERRY",re.IGNORECASE), re.compile("STEVE MADDEN",re.IGNORECASE), re.compile("GOTCHA",re.IGNORECASE), re.compile("ROBERT LEWIS",re.IGNORECASE), re.compile("Aldo",re.IGNORECASE), re.compile("American Abbey",re.IGNORECASE), re.compile("Apology",re.IGNORECASE), re.compile("Basement",re.IGNORECASE), re.compile("Cortefiel",re.IGNORECASE), re.compile("Dahla",re.IGNORECASE), re.compile("Denimlab",re.IGNORECASE), re.compile("Doo Australia",re.IGNORECASE), re.compile("Exit",re.IGNORECASE), re.compile("Guess",re.IGNORECASE), re.compile("Leonisa",re.IGNORECASE), re.compile("Levis",re.IGNORECASE), re.compile("Mango",re.IGNORECASE), re.compile("Mossimo",re.IGNORECASE), re.compile("Naf Naf",re.IGNORECASE), re.compile("Newport",re.IGNORECASE), re.compile("Pionier",re.IGNORECASE), re.compile("Stefano Cocci",re.IGNORECASE), re.compile("Sybilla",re.IGNORECASE), re.compile("Tommy Hilfiger",re.IGNORECASE), re.compile("University Club",re.IGNORECASE), re.compile("Vero moda",re.IGNORECASE), re.compile("Basement",re.IGNORECASE), re.compile("Bearcliff",re.IGNORECASE), re.compile("Calvin Klein",re.IGNORECASE), re.compile("Casio",re.IGNORECASE), re.compile("Christian Lacroix",re.IGNORECASE), re.compile("Denimlab",re.IGNORECASE), re.compile("Dockers",re.IGNORECASE), re.compile("Doo Australia",re.IGNORECASE), re.compile("Guess",re.IGNORECASE), re.compile("La Martina",re.IGNORECASE), re.compile("Mango",re.IGNORECASE), re.compile("Mossimo",re.IGNORECASE), re.compile("Newport",re.IGNORECASE), re.compile("Polo Ralph Lauren",re.IGNORECASE), re.compile("Ray Ban",re.IGNORECASE), re.compile("Riff&Raff",re.IGNORECASE), re.compile("Springfield",re.IGNORECASE), re.compile("Superdry",re.IGNORECASE), re.compile("Tommy Hilfiger",re.IGNORECASE), re.compile("University Club",re.IGNORECASE), re.compile("Wolf&Hank",re.IGNORECASE)
    ]}})

pro = [t1]  ## ARREGLO DE LOS QUERYS DE MONGO PARA MANDAR POR TELEGRAM
products = []

## FUNCION QUE COLOCA EN UNA LISTA (products) TODO LOS PRODUCTOS PARA SER MANDADOS A TELEGRAM,
## AQUI SE LE PASA EL OBJETO  MONGO PARA ITERACION Y EXTRACCIONDE LOS CAMPOS
def auto_telegram():
   
    db_collection1 = "voyager1"
    db_collection2 = "voyager2"
    for idx, value in enumerate(pro):

        for i in value:

            save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                            i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],db_collection1)
            # # se guarda en offer1  

            #products.append(mongo_obj)
            #print();print(i["sku"]);print(i["brand"]);print(i["product"]),print(i["link"])

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
                                , bot_tokey_key, chat_ide)

                print(" b no extiste")
                continue


            if b!=a:
                send_telegram( ("<b>Marca: "+i["brand"]+"</b>\nModelo: "+i["product"]+"\nPrecio Lista :" +str(i["list_price"])+ "\n<b>Precio web :"+str(i["best_price"])+"</b>\nPrecio Tarjeta :"+str(i["card_price"])+"\n"+i["image"]+"\nLink :"+str(i["link"]))  , bot_tokey_key, chat_ide)
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

