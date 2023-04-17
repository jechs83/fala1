import sys
import time
from html_test import html_code
import gc
from pymongo import MongoClient
import os
import pymongo
import re
import base64
import requests
from bd_compare import save_data_to_mongo_db
from decouple import config
from datetime import datetime
from telegram import ParseMode
import telegram
from pandas import DataFrame
import pandas as pd
from minimo import minimo
import pytz
import gc
from datetime import datetime
server_date = datetime.now()
timezone = pytz.timezone("America/Bogota")
peru_date = server_date.astimezone(timezone)
client = MongoClient(config("MONGO_DB"))
db5 = client["scrap"]
collection5 = db5["scrap"] 



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
        array_brand.append(i["brand"])
    print(array_brand)

    for i in t10:
            array_trash.append(i["trash"])
    print(array_trash)

    #for brand in array_brand:
     
    db = client["scrap"]
    collection = db["scrap"]
    db.command({"planCacheClear": "scrap"})

   
    

    t1 =  collection.find( {"web_dsct":{ "$gte":porcentage},"date":date ,"brand":{"$in":[ re.compile(brand,re.IGNORECASE) for brand in array_brand ]}, "product":{"$nin":[ re.compile(trash,re.IGNORECASE) for trash in array_trash ]}})
    t2 =  collection.find( {"best_price":{ "$gt": 0, "$lt": 51 },"date":date ,"brand":{"$in":[ re.compile(brand,re.IGNORECASE) for brand in array_brand ]}, "product":{"$nin":[ re.compile(trash,re.IGNORECASE) for trash in array_trash ]}})

                                                              
       
    collection_1 = db[ship_db1]
    collection_2 = db[ship_db2]

    for i in t1:
        product_array.append(i)
        print(i)
    
    for i in t2:
        product_array.append(i)
        print(i)



    for i in product_array:
            save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                           i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],ship_db1)
            f = print("se graba en bd datos")
            

            a= collection_1.find({"sku":i["sku"]})
            # se busca datos en offer1 cada iteracion
            a=list(a)
        
            b= collection_2.find({"sku":i["sku"]})
            # se busca datos en offer2  en cada iteracion 
            b = list(b)
            print(b)
            len_b = len(b)
            print(len_b)

            if len_b == 0:
                save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                            i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],ship_db2)
                

                if  i["card_price"] == 0:
                    card_price = ""
                else:
                    card_price = '\n👉Precio Tarjeta :'+str(i["card_price"])

                if i["web_dsct"] <= 50:
                    dsct = "🟡"
                if i["web_dsct"] > 50 and i["web_dsct"]  <=69:
                    dsct = "🟢"
                if i["web_dsct"] >=70:
                    dsct = "🔥"
                try:
                    historic = minimo(i["sku"])[3]
                except:
                    historic = False
                print(historic)

                if historic == True:

                    historic_min = "\n🔥🔥🔥🔥🔥🔥🔥 Minimo historico"
                    historic_list = "\nPrecio minimo: "+str(minimo(i["sku"])[0])+"\n"+"Precio anterior: "+str(minimo(i["sku"])[1])+"\n"+"Precio maximo: "+str(minimo(i["sku"])[2])
                if historic == False:

                    historic_min = ""
                    historic_list=""
                
                msn =  "✅Marca: "+str(i["brand"])+"\n✅"+str(i["product"])+"\n\n➡️Precio Lista :"+str(i["list_price"])+historic_min+"\n👉Precio web :"+str(i["best_price"])+historic_min+card_price+"\n"+dsct+"Descuento: "+"% "+str(i["web_dsct"])+"\n"+historic_list+"\n\n⌛"+i["date"]+" "+ i["time"]+"\n🔗Link :"+str(i["link"])+"\n🏠home web:"+i["home_list"]+"\n\n◀️◀️◀️◀️◀️◀️◀️▶️▶️▶️▶️▶️▶️"
                foto = i["image"]
                send_telegram(msn, foto, bot_token, chat_id)
                

                print(" PRODUCTO EN BASE B NO EXISTE, SE ENVIA A TELEGRAM")
                continue


            if b!=a:
                #send_telegram( ("<b>Marca: "+i["brand"]+"</b>\nModelo: "+i["product"]+"\nPrecio Lista :" +str(i["list_price"])+ "\n<b>Precio web :"+str(i["best_price"])+"</b>\nPrecio Tarjeta :"+str(i["card_price"])+"\n"+i["image"]+"\nLink :"+str(i["link"])))
                print("PRODUCTO DE A ES DIFERENTE DE B,  SE ENVIA  A TELEGRAM")
               
                save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                            i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],ship_db2)
                continue
            if a==b:
                print("SON IGUALES,  NO SE ENVIA TELEGRAM")
    gc.collect()




    print("se esta ejecutando")




db = client["brands"]
collection= db["tecno"]
t9 = collection.find({})

collection2= db["trash"]
t10 = collection2.find({})

array_trash=[]
array_brand= []
product_array = []

for i in t9:
    print(i)
    pattern = re.compile(str(i["brand"]), re.IGNORECASE)
    array_brand.append(pattern)
print(array_brand)

# pattern = re.compile(r"\bsecadora\b.*\blg\b", re.IGNORECASE)

# # Use the regular expression pattern in the pymongo query
# result = collection.find({"product": pattern, "date":"14/04/2023"})

# # Iterate through the query results
# for doc in result:
#     print(doc)