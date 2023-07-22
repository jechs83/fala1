import sys
import time
from html_test import html_code
import gc
from pymongo import MongoClient
import itertools
import re
import base64
import requests
import pymongo
from bd_compare import save_data_to_mongo_db
from decouple import config
from datetime import datetime
import telegram
from pandas import DataFrame
import pytz
from datetime import datetime

server_date = datetime.now()
timezone = pytz.timezone("America/Bogota")
peru_date = server_date.astimezone(timezone)

from pymongo import MongoClient
from decouple import config
client = MongoClient(config("MONGO_DB"))
#date = peru_date.strftime("%d/%m/%Y" )
#oferta_telegram = "👉 https://t.me/OfertasDescuentosPeru1 👈"
oferta_telegram = ""

#https://api.telegram.org/bot5573005249:AAFGCjc7zuI1XoHMqbd6gr1I1ZVi9Xd2I9s/sendMessage


def dia():
    now = datetime.now()
    date = now.strftime("%d/%m/%Y")
    #date = date.today()
    return date

date = dia()


def auto_telegram( category, ship_db1,ship_db2, bot_token, chat_id,porcentage):
    
    print("se esta ejecutando")
    db = client["brands"]
    collection= db[category]
    t9 = collection.find({})

    collection2= db["trash"]
    t10 = collection2.find({})
    
    array_trash=[]
    array_brand= []
    product_array = []

    for i in t9:
        pattern = re.compile(i["brand"], re.IGNORECASE)
        array_brand.append(pattern)
    print(array_brand)

    for i in t10:
        pattern = re.compile(i["trash"], re.IGNORECASE)
        array_trash.append(pattern)
    print(array_trash)

    print("Esta buscando en base de datos, puede tomar un tiempo")
     
    db = client["scrap"]
    collection = db["scrap"]
    # db.command({"planCacheClear": "scrap"})


    t1 =  collection.find( {"web_dsct":{ "$gte":porcentage},"date":date ,"brand":{"$in":array_brand}, "product":{"$nin":array_trash}})
    t2 =  collection.find( {"best_price":{ "$gt": 0, "$lt": 51 },"date":date ,"brand":{"$in":array_brand}, "product":{"$nin":array_trash}})

    # Concatenate the two cursors
    result = itertools.chain(t1, t2)
    # Iterate over the result and print each document
    for i in result:
    
        product_array.append(i)
        print(i)                                                          
       
    collection_1 = db[ship_db1]
    collection_2 = db[ship_db2]



    for i in product_array:
            save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                           i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],ship_db1)
            f = print("se graba en bd datos")
            



def auto_telegram_between_values(  ship_db1,ship_db2, bot_token, chat_id,porcentage1, porcentage2, producto):
    print("se esta ejecutando")
    product_array = []
    
    db = client["scrap"]
    collection = db["scrap"]
    db.command({"planCacheClear": "scrap"})

    t1 =  collection.find( {"web_dsct":{ "$gte":porcentage1, "$not":{"$gte":porcentage2}},"date":date , "product":{"$not":{"$in":[re.compile(producto,re.IGNORECASE),re.compile("reloj",re.IGNORECASE) ]} } })
    collection_1 = db[ship_db1]
    collection_2 = db[ship_db2]

    for i in t1:
        product_array.append(i)
        print(i)

    for i in product_array:
            try:
                save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                            i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],ship_db1)
                f = print("se graba en bd datos")
            except: continue
            

            a= collection_1.find({"sku":i["sku"]})
            # se busca datos en offer1 cada iteracion
            a=list(a)
        
            b= collection_2.find({"sku":i["sku"]})
            # se busca datos en offer2  en cada iteracion 
            b = list(b)
            #print(b)
            len_b = len(b)
            print(len_b)

            if len_b == 0:
                print(" NO EXSTE EN BASE DE DATOS ")
                try:
                    save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                                i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],ship_db2)
                except:
                     continue
            
        
      
client = MongoClient(config("MONGO_DB"))
TOKEN = config("CAPITAN_SULU_TOKEN")
chat_id = config("EXCELSIOR_CHAT_TOKEN")
bot_token = config("CAPITAN_SULU_TOKEN")
bd1 = "excelsior1"
bd2 = "excelsior2"
dsct = 60
dsct2 = 70
product  = "lentes"
db="scrap"
db_collection = "scrap"
    

#auto_telegram( category, bd1,bd2, bot_token, chat_id,dsct)


auto_telegram_between_values(  bd1,bd2, bot_token, chat_id,dsct, dsct2, product)
