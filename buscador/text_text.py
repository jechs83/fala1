
from html_test import html_code
import gc
from pymongo import MongoClient
import itertools
import re
import requests
from bd_compare import save_data_to_mongo_db
from decouple import config
from datetime import datetime
import pandas as pd
from minimo import minimo
import gc
from datetime import datetime
from decouple import config
client = MongoClient(config("MONGO_DB"))
TOKEN = config("RICHI_BOY_TOKEN")
chat_id = config("USS_DEFIANT")
bot_token = config("RICHI_BOY_TOKEN")

bd1 = "richi1"
bd2 = "richi2"
dsct = 60
product  = "lentes"
category = "tecno"

db="scrap"
db_collection = "scrap"
    
def hora():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

date = hora()

def send_telegram(message, foto, bot_token, chat_id):
    print("#########")
    print(foto)
    print("#########")
    if not foto:
        foto = "https://image.shutterstock.com/image-vector/no-image-available-sign-absence-260nw-373243873.jpg"

    if len(foto) <= 4:
        foto = "https://image.shutterstock.com/image-vector/no-image-available-sign-absence-260nw-373243873.jpg"

    # Create the inline button markup
    inline_button = {
        "inline_keyboard": [[{"text": "Forward", "callback_data": "forward"}]]
    }

    response = requests.post(
        f'https://api.telegram.org/bot{bot_token}/sendPhoto',
        data={'chat_id': chat_id, 'caption': str(message), "parse_mode": "HTML", "reply_markup": inline_button},
        files={'photo': requests.get(foto).content},
    )

def handle_callback(data, bot_token, chat_id):
    message_id = data['message']['message_id']
    forwarded_chat_id = "YOUR_FORWARD_CHAT_ID"  # Replace this with the target chat ID for forwarding
    response = requests.post(
        f'https://api.telegram.org/bot{bot_token}/forwardMessage',
        data={'chat_id': forwarded_chat_id, 'from_chat_id': chat_id, 'message_id': message_id}
    )

def buscador():

    
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
    
    dsct = 60
    t1 =  collection.find( {"web_dsct":{ "$gte":dsct},"date":date ,"brand":{"$in":array_brand}, "product":{"$nin":array_trash}})
    t2 =  collection.find( {"best_price":{ "$gt": 0, "$lt": 51 },"date":date ,"brand":{"$in":array_brand}, "product":{"$nin":array_trash}})

    # Concatenate the two cursors
    result = itertools.chain(t1, t2)


    # Iterate over the result and print each document
    for i in result:
    
        product_array.append(i)
        print(i)                                                          
       
    collection_1 = db[bd1]
    collection_2 = db[bd2]


    for i in product_array:
            save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                           i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],bd1)
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
                            i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],bd12)
                

                if  i["card_price"] == 0:
                    card_price = ""
                else:
                    card_price = '\n👉Precio Tarjeta :'+str(i["card_price"])

                if i["list_price"] == 0:
                        list_price = ""
                else:
                    list_price = '\n\n➡️Precio Lista :'+str(i["list_price"])

                if i["web_dsct"] <= 50:
                    dsct = "🟡"
                if i["web_dsct"] > 50 and i["web_dsct"]  <=69:
                    dsct = "🟢"
                if i["web_dsct"] >=70:
                    dsct = "🔥🔥🔥🔥🔥"

                historic_min = ""
                historic_list=""
                msn =  "✅Marca: "+str(i["brand"])+"\n✅"+str(i["product"])+list_price+"\n👉Precio web :"+str(i["best_price"])+card_price+"\n"+dsct+"Descuento: "+"% "+str(i["web_dsct"])+"\n"+"\n\n⌛"+i["date"]+" "+ i["time"]+"\n🔗Link :"+str(i["link"])+"\n🏠home web:"+i["home_list"]+"\n\n◀️◀️◀️◀️◀️◀️◀️▶️▶️▶️▶️▶️▶️"

        
                foto = i["image"]
                
                chat_id = config("DEEP_CHAT_TOKEN")

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

    buscador()
        


buscador()
