import time
import gc
from pymongo import MongoClient
import itertools
import re
import os
import requests
import time
from PIL import Image, ImageDraw, ImageFont
from telegram_search_dbSave import save_data_to_mongo_db

from decouple import config
from datetime import datetime
import pytz
from datetime import datetime

server_date = datetime.now()
timezone = pytz.timezone("America/Bogota")
peru_date = server_date.astimezone(timezone)

from pymongo import MongoClient
from decouple import config
client = MongoClient(config("MONGO_DB"))


def dia():
    now = datetime.now()
    date = now.strftime("%d/%m/%Y")
    #date = date.today()
    return date

date = dia()




# def send_telegram(message,foto, bot_token, chat_id):
   
    
#     if not foto:
#         foto="https://image.shutterstock.com/image-vector/no-image-available-sign-absence-260nw-373243873.jpg"
    
#     if len(foto)<=4:
#             foto="https://image.shutterstock.com/image-vector/no-image-available-sign-absence-260nw-373243873.jpg"    

   
#     response = requests.post(
        
#         f'https://api.telegram.org/bot{bot_token}/sendPhoto',
#         data={'chat_id': chat_id, 'caption': str(message), "parse_mode": "HTML"},
#         #files={'photo': requests.get(foto).content},
#         files={'photo': requests.get(foto).content},

#         )
 
#     print("se envio mensaje por funcion de telegram")


def send_telegram(message, foto, bot_token, chat_id):
    
    if not foto:
        foto = "https://image.shutterstock.com/image-vector/no-image-available-sign-absence-260nw-373243873.jpg"
    
    if len(foto) <= 4:
        foto = "https://image.shutterstock.com/image-vector/no-image-available-sign-absence-260nw-373243873.jpg"    
    
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Firefox/78.0'
        }      

    photo_response = requests.get(foto, headers=headers)

    
    photo_response = requests.get(foto)
    if photo_response.status_code == 403:
            foto= "https://image.shutterstock.com/image-vector/no-image-available-sign-absence-260nw-373243873.jpg"



    files = {'photo': ('photo.jpg', requests.get(foto).content)}
    
    
    response = requests.post(
        f'https://api.telegram.org/bot{bot_token}/sendPhoto',
        data={'chat_id': chat_id, 'caption': str(message), 'parse_mode': 'HTML'},
        files=files
    )
    response.raise_for_status()  # Check if the request was successful
    print("Message sent successfully")
  
      



def send_telegram_sin_imagen(message, bot_token, chat_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Firefox/78.0'
    }

    response = requests.post(
        f'https://api.telegram.org/bot{bot_token}/sendMessage',
        data={'chat_id': chat_id, 'text': str(message), 'parse_mode': 'HTML'},
    )
    
    response.raise_for_status()  # Check if the request was successful
    print("Message sent successfully")





def auto_telegram_between_values(  ship_db1,ship_db2, bot_token, chat_id,porcentage1, porcentage2,bd_name, collection_name):
    print("buscando")
   
    db = client[bd_name]
    collection = db[collection_name]
    collection_1 = db[ship_db1]
    collection_2 = db[ship_db2]

    ##########  OBTENGO LAS LISTAS DEL MONGO DE LOS PRODUCTOS CON EL RANGO DE DESCUENTO ##########
    live_search = collection.find({
        "$or": [
            {"web_dsct": {"$gte": porcentage1, "$lte": porcentage2}},
            {"card_dsct": {"$gte": porcentage1,  "$lte": porcentage2}},
        ],
        "date": date,
        # "product": {"$not": {"$in": [re.compile(producto, re.IGNORECASE), re.compile("reloj", re.IGNORECASE)]}}
            })
    #==================================================================================
    print("obtiene data de base principal")
    count = 0

    for i in live_search:
        count +=1
        print(i)

        data_live ={
               "sku": str(i["sku"]),
                "best_price":float(i["best_price"]),
                "list_price":float(i["list_price"]),
                "card_price":float(i["card_price"]),
                "web_dsct":float(i["web_dsct"]),
               "card_dsct": float(i["card_dsct"]),    
            }
        
        try:
            data_saved = collection_1.find_one({'sku': i['sku']})
        
            data_sv = {
                "sku": str(data_saved["sku"]),
                "best_price":float(data_saved["best_price"]),
                "list_price":float(data_saved["list_price"]),
                "card_price":float(data_saved["card_price"]),
                "web_dsct":float(data_saved["web_dsct"]),
                "card_dsct": float(data_saved["card_dsct"]),
            }
        except:
            data_sv = None  
      
   
        if data_live == data_sv:

            print("PRODUCTOS IGUALES, NO SE MANDA NADA A TELEGRAM Y NO DEBE GRABARSE TAMPOCO")
        
        if data_live != data_sv:

           

            if i["web_dsct"] <= 50:
                web_d = "🟡"
            if i["web_dsct"]  > 50 and i["web_dsct"]  <=69:
                web_d = "🟢"
            if i["web_dsct"]  >=70:
                web_d = "🔥🔥🔥🔥🔥🔥🔥"

            if i["card_dsct"] <= 50:
                card_d = "🟡"
            if i["card_dsct"] > 50 and i["card_dsct"]  <=69:
                card_d = "🟢"
            if i["card_dsct"]  >=70:
                card_d = "🔥🔥🔥🔥🔥🔥🔥"

            
            if i["list_price"] == 0:
                list_price = ""
            else:
                list_price = '🏷 <b>Precio lista:</b> '+  str(i["list_price"])+"\n" 
            
            if i["best_price"] == 0:
                best_price = ""
            else:
                best_price = '👉 <b>Precio web:</b> <b>'+ str(i["best_price"]) + "</b>" +"\n" 

            if i["card_price"] == 0:
                card_price = ""
            else:
                card_price = '💳 <b>Precio TC:</b> <b>' +str(i["card_price"])+ "</b>"+"\n" 

            if i["card_dsct"] == 0:
                card_dsct = ""
            else:
                card_dsct =  "💥 <b>Descuento TC:</b> %" + str(i["card_dsct"])+ card_d+"\n" 

            if i["web_dsct"] == 0:
                web_dsct = ""
            else:
                web_dsct =   "💵 <b>Descuento web:</b> %" + str(i["web_dsct"])+ web_d+  "\n" 
    
            foto = i["image"]

            if "http:" in foto:
                foto = foto.replace("http:", "https:")

            print(foto)
            if len(foto) <5:
        
                foto="https://westsiderc.org/wp-content/uploads/2019/08/Image-Not-Available.png"
            

            msn = (
               
                    "🌟🦙 <b>Detalles del Producto</b> 🦙🌟\n\n" +
                    "# sku: "+str(i["sku"]) + "\n" +
                    "✅ <b>Marca:</b> " + str(i["brand"]) + "\n" +
                    "📦 <b>Producto:</b> " + str(i["product"])  + "\n\n" +
                    str(list_price)+
                    str(best_price) +
                    str(card_price)+
                    "\n"+
                    str(card_dsct)+
                    str(web_dsct)+
                    "🏬 <b>Market:</b> " + str(i["market"]) + "\n" +
                    "🕗 <b>Fecha y Hora:</b> " + str(i["date"]) + " " + str(i["time"]) + "\n" +
                    "🔗 <b>Enlace:</b> <a href='" + str(i["link"]) + "'>Link aquí</a>\n\n" 
   
            )

        
            

            save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                        i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"], i["card_dsct"],bd_name,ship_db1)
            
               

            send_telegram (msn,foto, bot_token, chat_id)
         
          
            print("se debio enviar")
          
        


            print("LOS DATOS DEL PRODUCTO VARIO Y SE ENVIA A TELEGRAM  Y SE GUARDA EN LA BASE DE DTAOS DE COMPARACION")
            print("###################################################################################")
         


        if data_live == data_sv:

            print("LOS DATOS DEL PRODUCTO VARIO Y SE ENVIA A TELEGRAM  Y SE GUARDA EN LA BASE DE DTAOS DE COMPARACION")
        print( count)
    print("############      FIN     #############")
    gc.collect()

          
                
                
   
def productos_sin_dsct( ship_db1,ship_db2, bot_token, chat_id,bd_name, collection_name):

    db = client[bd_name]
    collection = db[collection_name]
    collection_1 = db[ship_db1]
    collection_2 = db[ship_db2]

   
    print("primer query")


    laptop_query1 = {
                    "$and": [
                        {"product": {"$regex": r'\b(ryzen\s7|ryzen\s5|ryzen\s9|8gb|16gb|12gb|32gb)\b', "$options": "i"}},
                        {"product": {"$regex": r'\b(laptop)\b', "$options": "i"}},
                        {"product": {"$regex": r'\b(16GB|12GB)\b', "$options": "i"}},
                        {"list_price": {"$lte": 2000}},
                        {"best_price": {"$lte": 2000}},
                        {"card_price": {"$lte": 2000}},
                        {"web_dsct":0},
                        {"card_dsct":0},
                        {"date": date},
                        {"product": {"$not": {"$regex": r'\b(reacondicionado|refurbished)\b', "$options": "i"}}},
                        ],
                        "$or":[
                                {"list_price": {"$ne": 0}},
                                {"best_price": {"$ne": 0}},
                                {"card_price": {"$ne": 0}}, ]
                    }
   
    
    laptop_query2 ={
                    "$and": [
                        {"product": {"$regex": r'\b(i\s7|i7|i\s5|i5|ci7|ci5|ci9|i\s9|i9)\b', "$options": "i"}},
                        {"product": {"$regex": r'\b(laptop)\b', "$options": "i"}},
                        {"product": {"$regex": r'\b(16GB|12GB)\b', "$options": "i"}},
                        {"list_price": {"$lte": 2000}},
                        {"best_price": {"$lte": 2000}},
                        {"card_price": {"$lte": 2000}},
                        {"web_dsct":0},
                        {"card_dsct":0},
                        {"date": date},
                        {"product": {"$not": {"$regex": r'\b(reacondicionado|refurbished)\b', "$options": "i"}}},
                    ],
                            "$or":[
                    
                                    {"list_price": {"$ne": 0}},
                                    {"best_price": {"$ne": 0}},
                                    {"card_price": {"$ne": 0}},
                               
                            ]
                }
    
    refri_query ={

                "$and": [
                        { "product": { "$regex": r'\b(refrigeradora|lavadora|cocina|)\b', "$options": "i"} },
                        { "brand": { "$regex": r'\b(samsung|lg|panasonic|sony|philips|hisense|indurama|bosch|oster|electrolux|coldex|daewoo|klimatic|mabe|sole|General\sElectric|Whirpool|frigidaire)\b', "$options": "i"} },
                        { "list_price": {"$lte": 1200 } },
                        { "best_price": { "$lte": 1200 } },
                        { "card_price": { "$lte": 1200 } },
                        {"web_dsct":0},
                        {"card_dsct":0},
                        {"date":date},
                    ],
          "$or":[
                {"list_price": {"$ne": 0}},
                {"best_price": {"$ne": 0}},
                {"card_price": {"$ne": 0}},
            ]
            }


    celular_query ={
                "$and": [
                    {"product": {"$regex": r'\b(smartphone|celular|6gb|8gb|12gb|tablet|ipad)\b', "$options": "i"}},
                    {"brand": {"$regex": r'\b(xiaomi|samsung|apple|lg|motorola|realme|oppo|vivo|redmi|honor|google|huawei|)\b', "$options": "i"}},
                    {"list_price": {"$lte": 1000}},
                    {"best_price": {"$lte": 1000}},
                    {"card_price": {"$lte": 1000}},
                    {"web_dsct":0},
                    {"card_dsct":0},
                    {"product": {"$not": {"$regex": r'\b(reacondicionado|refurbished)\b', "$options": "i"}}},
                    {"date": date},
                ],
          "$or":[
                {"list_price": {"$ne": 0}},
                {"best_price": {"$ne": 0}},
                {"card_price": {"$ne": 0}},
            ]
                    }

    tele_query = {
        "$and": [
        {"product": {"$regex": r"\b(televisor|tele|55\"|50\"|60\"|65\"|70\"|75\"|80\"|82\"|85\")\b", "$options": "i"}},
        {"brand": {"$regex": r"\b(samsung|lg|panasonic|sony|philips|hisense|tlc|aoc|xiaomi|aiwa)\b", "$options": "i"}},
        {"list_price": {"$lte": 1000, "$gt": 0}},
        {"best_price": {"$lte": 1000, "$gt": 0}},
        {"card_price": {"$lte": 1000, "$gt": 0}},
        {"web_dsct":0},
        {"card_dsct":0},
        {"product": {"$not": {"$regex": r'\b(reacondicionado|refurbished)\b', "$options": "i"}}},
        {"date": date},
   
    ],
          "$or":[
                {"list_price": {"$ne": 0}},
                {"best_price": {"$ne": 0}},
                {"card_price": {"$ne": 0}},
            ]
    }


    iphone_query = {
        "$and": [
            {"product": {"$regex": r"\b(iphone|pro|pro\smax|air|plus|macbook\spro|macbook)\b", "$options": "i"}},
            {"brand": {"$regex": r"\b(apple)\b", "$options": "i"}},
            {"list_price": {"$lte": 3000, "$gt": 0}},
            {"best_price": {"$lte": 3000, "$gt": 0}},
            {"card_price": {"$lte": 3000, "$gt": 0}},
            {"web_dsct":0},
            {"card_dsct":0},
            {"product": {"$not": {"$regex": r'\b(reacondicionado|refurbished|REACONDICIONADA)\b', "$options": "i"}}},
            {"date": date},
            {"$or": [
                {"list_price": {"$ne": 0}},
                {"best_price": {"$ne": 0}},
                {"card_price": {"$ne": 0}},
                 ]}
                ]
             }
    
    iphone_query2 = {
        "$and": [
            {"product": {"$regex": r"\b(iphone|pro|pro\smax|air|plus|macbook\spro|macbook)\b", "$options": "i"}},
            {"brand": {"$regex": r"\b(apple)\b", "$options": "i"}},
            {"list_price": {"$lte": 3000, "$gt": 0}},
            {"best_price": {"$lte": 3000, "$gt": 0}},
            {"card_price": {"$lte": 3000, "$gt": 0}},
            {"product": {"$not": {"$regex": r'\b(reacondicionado|refurbished|REACONDICIONADA)\b', "$options": "i"}}},
            {"date": date},
            {"$or": [
                {"list_price": {"$ne": 0}},
                {"best_price": {"$ne": 0}},
                {"card_price": {"$ne": 0}},
                 ]}
                ]
             }

    zapatilla_query = {
                    "$and": [
                
                        {"product": {"$regex": r'\b(zapatilla|zapatillas)\b', "$options": "i"}},
                        # {"brand": {"$regex": r'\b(nike|adidas|puma|converse|hi\stec|vans|reebok|)\b', "$options": "i"}},
                        # {"list_price": {"$lte": 150}},
                        # {"best_price": {"$lte": 150}},
                        # {"card_price": {"$lte": 150}},
                        {"web_dsct":{"$gte":50, "$lte":59}},
                        {"card_dsct":{"$lte":50, "$lte":59}},
                        {"date": date},
                        
                        ],

                        "$or":[
                
                                {"list_price": {"$ne": 0}},
                                {"best_price": {"$ne": 0}},
                                {"card_price": {"$ne": 0}},
                            ]
                    }
    
    zapatilla_query2 = {
                    "$and": [
                
                        {"product": {"$regex": r'\b(zapatilla|zapatillas)\b', "$options": "i"}},
                        # {"brand": {"$regex": r'\b(nike|adidas|puma|converse|hi\stec|vans|reebok|)\b', "$options": "i"}},
                        {"list_price": {"$lte": 150}},
                        {"best_price": {"$lte": 150}},
                        {"card_price": {"$lte": 150}},
                        {"web_dsct":0},
                        {"card_dsct":0},
                        {"date": date},
                        
                        ],

                        "$or":[
                
                                {"list_price": {"$ne": 0}},
                                {"best_price": {"$ne": 0}},
                                {"card_price": {"$ne": 0}},
                              
                        
                      
                            ]
                    }





    # # Execute the query
    # lap = collection.find(laptop)
    # sh = collection.find(shoes)
    # cel = collection.find(cel)
     
    # product_array = []
    # result = itertools.chain(lap, sh)


     # Execute the query
    lap1 = collection.find(laptop_query1)
    lap2 = collection.find(laptop_query2)
    cel = collection.find(celular_query)
    tele = collection.find(tele_query)
    iphone = collection.find(iphone_query)
    iphone2 = collection.find(iphone_query2)

    refri =collection.find(refri_query)
    zapatilla =collection.find(zapatilla_query)
    zapatilla2 =collection.find(zapatilla_query2)
     
    product_array = []
    result = itertools.chain(iphone, iphone2,zapatilla, zapatilla2,lap1 ,lap2, cel, tele, tele2, refri)
    #result = itertools.chain(iphone, iphone2)

  
     
    count = 0

    for i in result:
        print("obtiene data de base principal")
        count +=1
        print(i)

    

        data_live ={
               "sku": i["sku"],
                "best_price":i["best_price"],
                "list_price":i["list_price"],
                "card_price":i["card_price"],
                "web_dsct":i["web_dsct"],
               "card_dsct": i["card_dsct"],    
            }
        

        try:
            data_saved = collection_1.find_one({'sku': i['sku']})
        
            data_sv = {
                "sku": data_saved["sku"],
                "best_price":data_saved["best_price"],
                "list_price":data_saved["list_price"],
                "card_price":data_saved["card_price"],
                "web_dsct":data_saved["web_dsct"],
                "card_dsct": data_saved["card_dsct"],
            }
        except:
            data_sv = None

   
        if data_live == data_sv:

            print("PRODUCTOS IGUALES, NO SE MANDA NADA A TELEGRAM Y NO DEBE GRABARSE TAMPOCO")
        
        if data_live != data_sv:
           

            if i["web_dsct"] <= 50:
                web_d = "🟡"
            if i["web_dsct"]  > 50 and i["web_dsct"]  <=69:
                web_d = "🟢"
            if i["web_dsct"]  >=70:
                web_d = "🔥🔥🔥🔥🔥🔥🔥"

            if i["card_dsct"] <= 50:
                card_d = "🟡"
            if i["card_dsct"] > 50 and i["card_dsct"]  <=69:
                card_d = "🟢"
            if i["card_dsct"]  >=70:
                card_d = "🔥🔥🔥🔥🔥🔥🔥"

            
            if i["list_price"] == 0:
                list_price = ""
            else:
                list_price = '🏷 <b>Precio lista:</b> '+  str(i["list_price"])+"\n" 
            
            if i["best_price"] == 0:
                best_price = ""
            else:
                best_price = '👉 <b>Precio web:</b> <b>'+ str(i["best_price"]) + "</b>" +"\n" 

            if i["card_price"] == 0:
                card_price = ""
            else:
                card_price = '💳 <b>Precio TC:</b> <b>' +str(i["card_price"])+ "</b>"+"\n" 

            if i["card_dsct"] == 0:
                card_dsct = ""
            else:
                card_dsct =  "💥 <b>Descuento TC:</b> %" + str(i["card_dsct"])+ card_d+"\n" 

            if i["web_dsct"] == 0:
                web_dsct = ""
            else:
                web_dsct =   "💵 <b>Descuento web:</b> %" + str(i["web_dsct"])+ web_d+  "\n" 
    
            if list_price and best_price and card_price == 0:
                continue
            

            msn = (
                
                    "🌟🦙 <b>Detalles del Producto</b> 🦙🌟\n\n" +
                    str(i["image"])+"\n" +
                    "✅ <b>Marca:</b> " + str(i["brand"]) + "\n" +
                    "📦 <b>Producto:</b> " + str(i["product"])  + "\n\n" +
                    list_price+
                    best_price +
                    card_price+
                    "\n"+
                    card_dsct+
                    web_dsct+
                    "🏬 <b>Market:</b> " + i["market"] + "\n" +
                    "🕗 <b>Fecha y Hora:</b> " + i["date"] + " " + i["time"] + "\n" +
                    "🔗 <b>Enlace:</b> <a href='" + str(i["link"]) + "'>Link aquí</a>\n\n" 
            )


            foto = i["image"]

            if len(foto) <5:
        
                foto="https://westsiderc.org/wp-content/uploads/2019/08/Image-Not-Available.png"

            save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                        i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"], i["card_dsct"],bd_name,ship_db1)
            
            send_telegram (msn, foto, bot_token, chat_id)
        


            print("LOS DATOS DEL PRODUCTO VARIO Y SE ENVIA A TELEGRAM  Y SE GUARDA EN LA BASE DE DTAOS DE COMPARACION")
            print("###################################################################################")
         


        if data_live == data_sv:

            print("LOS DATOS DEL PRODUCTO VARIO Y SE ENVIA A TELEGRAM  Y SE GUARDA EN LA BASE DE DTAOS DE COMPARACION")
        print( count)
        print("############      FIN     #############")



def auto_product(  ship_db1,ship_db2, bot_token, chat_id,porcentage1, porcentage2, product):
    db = client["saga"]
    collection = db["scrap"]
    db2 = client["ripley"]
    collection2 = db2["scrap"]
    collection_1 = db[ship_db1]
    collection_2 = db[ship_db2]
    producto = product


    query ={
            "$and": [
                {"product": {"$regex": r'\b(zapatilla)\b', "$options": "i"}},
                {"product": {"$in":["/"+product+"/i"]}},

                # {"brand": {"$regex": r'\b(xiaomi|samsung|apple|lg|motorola|realme|oppo|vivo|redmi|honor|google|huawei|)\b', "$options": "i"}},
                {"date": date},
                
            ],
        "$or":[
                {"web_dsct":{"gte":porcentage1, "$lte":porcentage2}},
                {"card_dsct":{"gte":porcentage1, "$lte":porcentage2}},
        
        ]
                }

    search = collection.find(query)
    search2 = collection2.find(query)
    print(search)
    print(search2)
    arr = []
    for i in search:
        arr.append(i)

    print(arr)
    result = itertools.chain(search2 ,search)
    
     
    count = 0

    for i in result:
        print("obtiene data de base principal")
        count +=1
        print(i)
        
        
           

        if i["web_dsct"] <= 50:
            web_d = "🟡"
        if i["web_dsct"]  > 50 and i["web_dsct"]  <=69:
            web_d = "🟢"
        if i["web_dsct"]  >=70:
            web_d = "🔥🔥🔥🔥🔥🔥🔥"

        if i["card_dsct"] <= 50:
            card_d = "🟡"
        if i["card_dsct"] > 50 and i["card_dsct"]  <=69:
            card_d = "🟢"
        if i["card_dsct"]  >=70:
            card_d = "🔥🔥🔥🔥🔥🔥🔥"

        
        if i["list_price"] == 0:
            list_price = ""
        else:
            list_price = '🏷 <b>Precio lista:</b> '+  str(i["list_price"])+"\n" 
        
        if i["best_price"] == 0:
            best_price = ""
        else:
            best_price = '👉 <b>Precio web:</b> <b>'+ str(i["best_price"]) + "</b>" +"\n" 

        if i["card_price"] == 0:
            card_price = ""
        else:
            card_price = '💳 <b>Precio TC:</b> <b>' +str(i["card_price"])+ "</b>"+"\n" 

        if i["card_dsct"] == 0:
            card_dsct = ""
        else:
            card_dsct =  "💥 <b>Descuento TC:</b> %" + str(i["card_dsct"])+ card_d+"\n" 

        if i["web_dsct"] == 0:
            web_dsct = ""
        else:
            web_dsct =   "💵 <b>Descuento web:</b> %" + str(i["web_dsct"])+ web_d+  "\n" 

        if list_price and best_price and card_price == 0:
            continue
        

        msn = (
            
                "🌟🦙 <b>Detalles del Producto</b> 🦙🌟\n\n" +
                "✅ <b>Marca:</b> " + str(i["brand"]) + "\n" +
                "📦 <b>Producto:</b> " + str(i["product"])  + "\n\n" +
                list_price+
                best_price +
                card_price+
                "\n"+
                card_dsct+
                web_dsct+
                "🏬 <b>Market:</b> " + i["market"] + "\n" +
                "🕗 <b>Fecha y Hora:</b> " + i["date"] + " " + i["time"] + "\n" +
                "🔗 <b>Enlace:</b> <a href='" + str(i["link"]) + "'>Link aquí</a>\n\n" 
        )


        foto = i["image"]

        if len(foto) <5:
    
            foto="https://westsiderc.org/wp-content/uploads/2019/08/Image-Not-Available.png"


        send_telegram (msn, foto, bot_token, chat_id)
    


        print("LOS DATOS DEL PRODUCTO VARIO Y SE ENVIA A TELEGRAM  Y SE GUARDA EN LA BASE DE DTAOS DE COMPARACION")
        print("###################################################################################")

