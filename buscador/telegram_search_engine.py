import time
import gc
from pymongo import MongoClient
import itertools
import re
import requests
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


def send_telegram(message,foto, bot_token, chat_id):

    if not foto:
        foto="https://image.shutterstock.com/image-vector/no-image-available-sign-absence-260nw-373243873.jpg"
    
    if len(foto)<=4:
            foto="https://image.shutterstock.com/image-vector/no-image-available-sign-absence-260nw-373243873.jpg"

    response = requests.post(
        
        f'https://api.telegram.org/bot{bot_token}/sendPhoto',
        data={'chat_id': chat_id, 'caption': str(message), "parse_mode": "HTML"},
        files={'photo': requests.get(foto).content},
    
        )
    print("se envio mensaje por funcion de telegram")



def auto_telegram_between_values(  ship_db1,ship_db2, bot_token, chat_id,porcentage1, porcentage2, producto, bd_name, collection_name):
    print("buscando")
   
    db = client[bd_name]
    collection = db[collection_name]
    collection_1 = db[ship_db1]

    ##########  OBTENGO LAS LISTAS DEL MONGO DE LOS PRODUCTOS CON EL RANGO DE DESCUENTO ##########
    live_search = collection.find({
        "$or": [
            {"web_dsct": {"$gte": porcentage1, "$lte": porcentage2}},
            {"card_dsct": {"$gte": porcentage1,  "$lte": porcentage2}},
        ],
        "date": date,
        "product": {"$not": {"$in": [re.compile(producto, re.IGNORECASE), re.compile("reloj", re.IGNORECASE)]}}
            })
    #==================================================================================
    print("obtiene data de base principal")
    count = 0

    for i in live_search:
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

            save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                        i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"], i["card_dsct"],bd_name,ship_db1)
            
            send_telegram (msn, foto, bot_token, chat_id)
        


            print("LOS DATOS DEL PRODUCTO VARIO Y SE ENVIA A TELEGRAM  Y SE GUARDA EN LA BASE DE DTAOS DE COMPARACION")
            print("###################################################################################")
         


        if data_live == data_sv:

            print("LOS DATOS DEL PRODUCTO VARIO Y SE ENVIA A TELEGRAM  Y SE GUARDA EN LA BASE DE DTAOS DE COMPARACION")
        print( count)
    print("############      FIN     #############")

          
                
                
   
def productos_sin_dsct( ship_db1,ship_db2, bot_token, chat_id,bd_name, collection_name):

    db = client[bd_name]
    collection = db[collection_name]

    product_shoes_patters =[
                    re.compile(r'zapatilla', re.IGNORECASE),
                    re.compile(r'sandalia', re.IGNORECASE),
                    re.compile(r'zapato', re.IGNORECASE),
            ]

    # Define the brand regex patterns
    brand_shoes_patterns = [
        re.compile(r'puma', re.IGNORECASE),
        re.compile(r'adidas', re.IGNORECASE),
        re.compile(r'reebok', re.IGNORECASE),
        re.compile(r'nike', re.IGNORECASE),
        re.compile(r'under armor', re.IGNORECASE),
        re.compile(r'hi tec', re.IGNORECASE),
        re.compile(r'Converse', re.IGNORECASE),
        re.compile(r'vans', re.IGNORECASE)
    ]

    # Define the query
    shoes = {
        "product": {"$in": product_shoes_patters},
        "brand": {"$in": brand_shoes_patterns},
        "$or": [
            {"best_price": {"$lte": 150, "$gt": 0}},
            {"list_price": {"$lte": 150, "$gt": 0}},
            {"card_price": {"$lte": 150, "$gt": 0}}
        ]
    }

    #################################################\
    product_compu_regex_patterns = [
    re.compile(r'laptop', re.IGNORECASE),
    re.compile(r'ryzen', re.IGNORECASE),
    re.compile(r'notebook', re.IGNORECASE),
    re.compile(r'tablet', re.IGNORECASE),
    re.compile(r'ipad', re.IGNORECASE)
    ]

    # Define the exclusion patterns
    exclusion_compu_patterns = [
        re.compile(r'celeron', re.IGNORECASE),
        re.compile(r'ryzen 3', re.IGNORECASE),
        re.compile(r'core i3', re.IGNORECASE),
        re.compile(r'ci3', re.IGNORECASE)
    ]

    # Define the brand regex patterns
    brand_compu_patterns = [
        re.compile(r'lenovo', re.IGNORECASE),
        re.compile(r'alien', re.IGNORECASE),
        re.compile(r'hp', re.IGNORECASE),
        re.compile(r'lg', re.IGNORECASE),
        re.compile(r'apple', re.IGNORECASE),
        re.compile(r'asus', re.IGNORECASE),
        re.compile(r'acer', re.IGNORECASE),
        re.compile(r'panasonic', re.IGNORECASE)
    ]

    # Define the query
    laptop = {
        "product": {
            "$in": product_compu_regex_patterns,
            "$not": {"$in": exclusion_compu_patterns}
        },
        "brand": {"$in": brand_compu_patterns},
        "web_dsct": 0,
        "$or": [
            {"best_price": {"$lte": 3500, "$gt": 0}},
            {"list_price": {"$lte": 3500, "$gt": 0}},
            {"card_price": {"$lte": 3500, "$gt": 0}}
        ]
    }


    # Execute the query
    lap = collection.find(laptop)
    sh = collection.find(shoes)
     
    product_array = []
    result = itertools.chain(lap, sh)
    # Iterate over the result and print each document
    for i in result:
    
        product_array.append(i)
        print(i)     
    collection_1 = db[ship_db1]
    collection_2 = db[ship_db2]
    for i in product_array:
            save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                           i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],bd_name,ship_db1)
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
                            i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],bd_name,ship_db2)
                

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
                
                msn = (
                  
                        "🌟🦙 <b>Detalles del Producto</b> 🦙🌟\n\n" +
                        "✅ <b>Marca:</b> " + str(i["brand"]) + "\n" +
                        "📦 <b>Producto:</b> " + str(i["product"]) + list_price + "\n" +
                        "👉 <b>Precio web:</b> " + str(i["best_price"]) + card_price + "\n" +
                        "🏷 <b>Descuento:</b> %" + str(i["web_dsct"]) + " " + dsct + "\n\n" +
                        "🕗 <b>Fecha y Hora:</b> " + i["date"] + " " + i["time"] + "\n" +
                        "🔗 <b>Enlace:</b> <a href='" + str(i["link"]) + "'>Link aquí</a>\n\n" 
                    )

                # msn =  "✅Marca: "+str(i["brand"])+"\n✅"+str(i["product"])+list_price+"\n👉Precio web :"+str(i["best_price"])+card_price+"\n"+dsct+"Descuento: "+"% "+str(i["web_dsct"])+"\n"+"\n\n⌛"+i["date"]+" "+ i["time"]+"\n🔗Link :"+str(i["link"])+"\n🏠home web:"+i["home_list"]+"\n\n◀️◀️◀️◀️◀️◀️◀️▶️▶️▶️▶️▶️▶️"
                foto = i["image"]
                send_telegram(msn, foto, bot_token, chat_id)
                print(chat_id)
                print(bot_token)
                print(" PRODUCTO EN BASE B NO EXISTE, SE ENVIA A TELEGRAM")
                


            if b!=a:
                #send_telegram( ("<b>Marca: "+i["brand"]+"</b>\nModelo: "+i["product"]+"\nPrecio Lista :" +str(i["list_price"])+ "\n<b>Precio web :"+str(i["best_price"])+"</b>\nPrecio Tarjeta :"+str(i["card_price"])+"\n"+i["image"]+"\nLink :"+str(i["link"])))
                print("PRODUCTO DE A ES DIFERENTE DE B,  SE ENVIA  A TELEGRAM")
               
                save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                            i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],bd_name,ship_db2)
                continue
            if a==b:
                print("SON IGUALES,  NO SE ENVIA TELEGRAM")


          
           








