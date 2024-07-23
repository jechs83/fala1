import time
import gc
from pymongo import MongoClient
import itertools
import re
import os
import requests
import time

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




# def send_telegram(message, foto, bot_token, chat_id):
    
#     if not foto:
#         foto = "https://image.shutterstock.com/image-vector/no-image-available-sign-absence-260nw-373243873.jpg"
    
#     if len(foto) <= 4:
#         foto = "https://image.shutterstock.com/image-vector/no-image-available-sign-absence-260nw-373243873.jpg"  
        
          
    
#     headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Firefox/78.0'
#         }      

#     photo_response = requests.get(foto, headers=headers)

    
#     photo_response = requests.get(foto)
#     if photo_response.status_code == 403:
#             foto= "https://image.shutterstock.com/image-vector/no-image-available-sign-absence-260nw-373243873.jpg"



#     files = {'photo': ('photo.jpg', requests.get(foto).content)}
    
    
#     response = requests.post(
#         f'https://api.telegram.org/bot{bot_token}/sendPhoto',
#         data={'chat_id': chat_id, 'caption': str(message), 'parse_mode': 'HTML'},
#         files=files
#     )
#     response.raise_for_status()  # Check if the request was successful
#     print("Message sent successfully")
  
  ######################################################################################################    

# def send_telegram(message, foto, bot_token, chat_id):
    
#     try:
#         if not foto:
#             foto = "https://image.shutterstock.com/image-vector/no-image-available-sign-absence-260nw-373243873.jpg"
        
#         if len(foto) <= 4:
#             foto = "https://image.shutterstock.com/image-vector/no-image-available-sign-absence-260nw-373243873.jpg" 

#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
#             'Referer': 'https://home.ripley.com.pe'
#         }
#         response = requests.get(foto, headers=headers)
#         response.raise_for_status()
#         photo_data = response.content
        
#         # Send photo using Telegram API
#         telegram_response = requests.post(
#             f'https://api.telegram.org/bot{bot_token}/sendPhoto',
#             data={'chat_id': chat_id, 'caption': str(message), "parse_mode": "HTML"},
#             files={'photo': photo_data},
#         )
        
#         telegram_response.raise_for_status()
#         print("SE ENVIO MENSAJE POR TELEGRAM.")
#     except requests.exceptions.RequestException as e:
#         print("ERROR ENE L REQUEST DE IMAGEN:", e)
#     except Exception as e:
#         print("ERROR AL ENVIAR :", e)
  


def send_telegram(message, foto, bot_token, chat_id, max_retries=5):
    if not foto:
        foto = "https://image.shutterstock.com/image-vector/no-image-available-sign-absence-260nw-373243873.jpg"
    
    if len(foto) <= 4:
        foto = "https://image.shutterstock.com/image-vector/no-image-available-sign-absence-260nw-373243873.jpg"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'Referer': 'https://home.ripley.com.pe'
    }

    retries = 0
    backoff = 1  # backoff inicial en segundos

    while retries < max_retries:
        try:
            response = requests.get(foto, headers=headers)
            response.raise_for_status()
            photo_data = response.content

            # Send photo using Telegram API
            telegram_response = requests.post(
                f'https://api.telegram.org/bot{bot_token}/sendPhoto',
                data={'chat_id': chat_id, 'caption': str(message), "parse_mode": "HTML"},
                files={'photo': ('photo.jpg', photo_data)},
            )

            telegram_response.raise_for_status()
            print("SE ENVIO MENSAJE POR TELEGRAM.")
            return  # Salir de la función si se envía el mensaje con éxito

        except requests.exceptions.HTTPError as e:
            if telegram_response.status_code == 429:
                retries += 1
                print(f"Error 429: Too Many Requests. Retrying in {backoff} seconds...")
                time.sleep(backoff)
                backoff *= 2  # Incrementa el backoff exponencialmente
            else:
                print(f"HTTP Error: {e}")
                break
        except requests.exceptions.RequestException as e:
            print("ERROR EN EL REQUEST DE IMAGEN:", e)
            break
        except Exception as e:
            print("ERROR AL ENVIAR:", e)
            break

    print("Max retries reached. Exiting.")



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

          
###################################################################################
# FUNCION QUE CREA EXLUSIONES Y FILTROS DETALLADOS PARA LOS PRODUCTOS ##

def build_query(conditions, exclusions, date, max_price=None):
    query = {"$and": conditions + [{"date": date}]}
    
    if exclusions:
        for exclusion in exclusions:
            query["$and"].append({"product": {"$not": {"$regex": exclusion, "$options": "i"}}})
    
    if max_price:
        price_conditions = [
            {"list_price": {"$lte": max_price}},
            {"best_price": {"$lte": max_price}},
            {"card_price": {"$lte": max_price}}
        ]
        query["$and"].extend(price_conditions)
    
    query["$or"] = [
        {"list_price": {"$ne": 0}},
        {"best_price": {"$ne": 0}},
        {"card_price": {"$ne": 0}}
    ]
    
    return query
                
######################################################################             
   
def productos_sin_dsct( ship_db1,ship_db2, bot_token, chat_id,bd_name, collection_name):

    db = client[bd_name]
    collection = db[collection_name]
    collection_1 = db[ship_db1]
    collection_2 = db[ship_db2]

   
    print("primer query")


    queries = {
        # "laptop_query1": build_query(
        #     conditions=[
        #         {"product": {"$regex": r'\b(ryzen\s7|ryzen\s5|ryzen\s9)\b', "$options": "i"}},
        #           {"product": {"$regex": r'\b(galaxy|)\b', "$options": "i"}},
        #         #{"product": {"$regex": r'\b(rtx|gtx|)\b', "$options": "i"}},
        #         #{"product": {"$regex": r'\b(laptop)\b', "$options": "i"}},
        #         # {"product": {"$regex": r'\b(16GB|12GB)\b', "$options": "i"}},
        #         {"web_dsct": 0},
        #         {"card_dsct": 0},
        #     ],
        #     exclusions=[r'\b(reacondicionado|refurbished)\b'],
        #     date=date,
        #     max_price=3000
        # ),
         "query3" : build_query(
            conditions=[
                 #{"product": {"$regex": r'\b(ryzen\s7|ryzen\s5|ryzen\s9)\b', "$options": "i"}},
                {"product": {"$regex": r'\b(refrigeradora)\b', "$options": "i"}},
            
                {"$or": [
                    {"list_price": {"$gt": 0}, "best_price": 0, "card_price": 0},
                    {"list_price": 0, "best_price": {"$gt": 0}, "card_price": 0},
                    {"list_price": 0, "best_price": 0, "card_price": {"$gt": 0}},
                ]}
                    ],
                    exclusions=[r'\b(reacondicionado|refurbished)\b'],
                    date=date,
                    max_price=1500
                        ),


        "query2" : build_query(
            conditions=[
                 #{"product": {"$regex": r'\b(ryzen\s7|ryzen\s5|ryzen\s9)\b', "$options": "i"}},
                {"product": {"$regex": r'\b(iphone\15|iphone\14|iphone\13)\b', "$options": "i"}},
                



                {"$or": [
                    {"list_price": {"$gt": 0}, "best_price": 0, "card_price": 0},
                    {"list_price": 0, "best_price": {"$gt": 0}, "card_price": 0},
                    {"list_price": 0, "best_price": 0, "card_price": {"$gt": 0}},
                ]}
                    ],
                    exclusions=[r'\b(reacondicionado|refurbished)\b'],
                    date=date,
                    max_price=2700
                        ),


      "query1" : build_query(
            conditions=[
                 #{"product": {"$regex": r'\b(ryzen\s7|ryzen\s5|ryzen\s9)\b', "$options": "i"}},
                #{"product": {"$regex": r'\b(iphone\15|iphone\14|iphone\13)\b', "$options": "i"}},
                {"product": {"$regex": r'\b(televisor)\b', "$options": "i"}},



                {"$or": [
                    {"list_price": {"$gt": 0}, "best_price": 0, "card_price": 0},
                    {"list_price": 0, "best_price": {"$gt": 0}, "card_price": 0},
                    {"list_price": 0, "best_price": 0, "card_price": {"$gt": 0}},
                ]}
                    ],
                    exclusions=[r'\b(reacondicionado|refurbished)\b'],
                    date=date,
                    max_price=1400
                        ),


        "query4" : build_query(
            conditions=[
                 #{"product": {"$regex": r'\b(ryzen\s7|ryzen\s5|ryzen\s9)\b', "$options": "i"}},
                #{"product": {"$regex": r'\b(iphone\15|iphone\14|iphone\13)\b', "$options": "i"}},
                {"product": {"$regex": r'\b(macbook|mini\smac)\b', "$options": "i"}},



                {"$or": [
                    {"list_price": {"$gt": 0}, "best_price": 0, "card_price": 0},
                    {"list_price": 0, "best_price": {"$gt": 0}, "card_price": 0},
                    {"list_price": 0, "best_price": 0, "card_price": {"$gt": 0}},
                ]}
                    ],
                    exclusions=[r'\b(reacondicionado|refurbished)\b'],
                    date=date,
                    max_price=3500
                        ),


            "query5" : build_query(
            conditions=[
                 #{"product": {"$regex": r'\b(ryzen\s7|ryzen\s5|ryzen\s9)\b', "$options": "i"}},
                #{"product": {"$regex": r'\b(iphone\15|iphone\14|iphone\13)\b', "$options": "i"}},
                {"product": {"$regex": r'\b(cocina)\b', "$options": "i"}},

                {"$or": [
                    {"list_price": {"$gt": 0}, "best_price": 0, "card_price": 0},
                    {"list_price": 0, "best_price": {"$gt": 0}, "card_price": 0},
                    {"list_price": 0, "best_price": 0, "card_price": {"$gt": 0}},
                ]}
                    ],
                    exclusions=[r'\b(reacondicionado|refurbished)\b'],
                    date=date,
                    max_price=700
                        ),


               "query6" : build_query(
            conditions=[
                 #{"product": {"$regex": r'\b(ryzen\s7|ryzen\s5|ryzen\s9)\b', "$options": "i"}},
                #{"product": {"$regex": r'\b(iphone\15|iphone\14|iphone\13)\b', "$options": "i"}},
                {"product": {"$regex": r'\b(galaxy\ss24|galaxy\ss23|galaxy\ss22)\b', "$options": "i"}},

                {"$or": [
                    {"list_price": {"$gt": 0}, "best_price": 0, "card_price": 0},
                    {"list_price": 0, "best_price": {"$gt": 0}, "card_price": 0},
                    {"list_price": 0, "best_price": 0, "card_price": {"$gt": 0}},
                ]}
                    ],
                    exclusions=[r'\b(reacondicionado|refurbished)\b'],
                    date=date,
                    max_price=2400
                        ),


              "query7" : build_query(
            conditions=[
                 #{"product": {"$regex": r'\b(ryzen\s7|ryzen\s5|ryzen\s9)\b', "$options": "i"}},
                #{"product": {"$regex": r'\b(iphone\15|iphone\14|iphone\13)\b', "$options": "i"}},
                {"product": {"$regex": r'\b(parlante)\b', "$options": "i"}},
                {"brand": {"$regex": r'\b(samsung|lg|sonos|bose|apple|sony)\b', "$options": "i"}},


                {"$or": [
                    {"list_price": {"$gt": 0}, "best_price": 0, "card_price": 0},
                    {"list_price": 0, "best_price": {"$gt": 0}, "card_price": 0},
                    {"list_price": 0, "best_price": 0, "card_price": {"$gt": 0}},
                ]}
                    ],
                    exclusions=[r'\b(reacondicionado|refurbished)\b'],
                    date=date,
                    max_price=400
                        ),



                   "query7" : build_query(
            conditions=[
                 #{"product": {"$regex": r'\b(ryzen\s7|ryzen\s5|ryzen\s9)\b', "$options": "i"}},
                #{"product": {"$regex": r'\b(iphone\15|iphone\14|iphone\13)\b', "$options": "i"}},
                {"product": {"$regex": r'\b(zapatillas)\b', "$options": "i"}},
                 {"brand": {"$regex": r'\b(adidas|nike|reebok|guess|skechers|puma)\b', "$options": "i"}},
                {"$or": [
                    {"list_price": {"$gt": 0}, "best_price": 0, "card_price": 0},
                    {"list_price": 0, "best_price": {"$gt": 0}, "card_price": 0},
                    {"list_price": 0, "best_price": 0, "card_price": {"$gt": 0}},
                ]}
                    ],
                    exclusions=[r'\b(reacondicionado|refurbished)\b'],
                    date=date,
                    max_price=100
                        ),


        # "laptop_query3": build_query(
        #     conditions=[
        #         {"product": {"$regex": r'\b(macbook|mini\smac|)\b', "$options": "i"}},
        #         {"web_dsct": 0},
        #         {"card_dsct": 0},
        #     ],
        #     exclusions=[r'\b(reacondicionado|refurbished)\b'],
        #     date=date,
        #     max_price=3500
        # ),
        # "refri_query": build_query(
        #     conditions=[
        #         {"product": {"$regex": r'\b(refrigeradora|lavadora|cocina|)\b', "$options": "i"}},
        #         #{"brand": {"$regex": r'\b(samsung|lg|panasonic|sony|philips|hisense|indurama|bosch|oster|electrolux|coldex|daewoo|klimatic|mabe|sole|General\sElectric|Whirpool|frigidaire)\b', "$options": "i"}},
        #         {"web_dsct": 0},
        #         {"card_dsct": 0},
        #     ],
        #     exclusions=[],
        #     date=date,
        #     max_price=1200
        # ),
        # "celular_query": build_query(
        #     conditions=[
        #         {"product": {"$regex": r'\b(smartphone|celular|tablet)\b', "$options": "i"}},
        #         #{"brand": {"$regex": r'\b(xiaomi|samsung|apple|lg|motorola|realme|oppo|vivo|redmi|honor|google|huawei|)\b', "$options": "i"}},
        #         {"web_dsct": 0},
        #         {"card_dsct": 0},
        #     ],
        #     exclusions=[r'\b(reacondicionado|refurbished)\b'],
        #     date=date,
        #     max_price=1000
        # ),
        # "tele_query": build_query(
        #     conditions=[
        #         {"product": {"$regex": r'\b(televisor|tele|55\"|50\"|60\"|65\"|70\"|75\"|80\"|82\"|85\")\b', "$options": "i"}},
        #         #{"brand": {"$regex": r'\b(samsung|lg|panasonic|sony|philips|hisense|tlc|aoc|xiaomi|aiwa)\b', "$options": "i"}},
        #         {"web_dsct": 0},
        #         {"card_dsct": 0},
        #     ],
        #     exclusions=[r'\b(reacondicionado|refurbished)\b'],
        #     date=date,
        #     max_price=1000
        # ),
        # "iphone_query": build_query(
        #     conditions=[
        #         {"product": {"$regex": r'\b(iphone|pro|pro\smax|air|plus|macbook\spro|macbook)\b', "$options": "i"}},
        #         {"brand": {"$regex": r'\b(apple)\b', "$options": "i"}},
        #         {"web_dsct": 0},
        #         {"card_dsct": 0},
        #     ],
        #     exclusions=[r'\b(reacondicionado|refurbished|REACONDICIONADA)\b'],
        #     date=date,
        #     max_price=3000
        # ),
      
        # "zapatilla_query2": build_query(
        #     conditions=[
        #         {"product": {"$regex": r'\b(zapatilla|zapatillas)\b', "$options": "i"}},
        #         {"web_dsct": 0},
        #         {"card_dsct": 0},
        #     ],
        #     exclusions=[],
        #     date=date,
        #     max_price=150
        # )
    }



     # Execute the query
    results = itertools.chain(
        *[collection.find(query) for query in queries.values()]
    )

    for i in results:
        data_live = {
            "sku": i["sku"],
            "best_price": i["best_price"],
            "list_price": i["list_price"],
            "card_price": i["card_price"],
            "web_dsct": i["web_dsct"],
            "card_dsct": i["card_dsct"],
        }

        data_saved = collection_1.find_one({'sku': i['sku']})

        if data_saved:
            data_sv = {
                "sku": data_saved["sku"],
                "best_price": data_saved["best_price"],
                "list_price": data_saved["list_price"],
                "card_price": data_saved["card_price"],
                "web_dsct": data_saved["web_dsct"],
                "card_dsct": data_saved["card_dsct"],
            }
        else:
            data_sv = None

        if data_live != data_sv:
            web_d = "🔥" if i["web_dsct"] >= 70 else "🟢" if i["web_dsct"] > 50 else "🟡"
            card_d = "🔥" if i["card_dsct"] >= 70 else "🟢" if i["card_dsct"] > 50 else "🟡"
            
            list_price = f'🏷 <b>Precio lista:</b> {i["list_price"]}\n' if i["list_price"] != 0 else ""
            best_price = f'👉 <b>Precio web:</b> <b>{i["best_price"]}</b>\n' if i["best_price"] != 0 else ""
            card_price = f'💳 <b>Precio TC:</b> <b>{i["card_price"]}</b>\n' if i["card_price"] != 0 else ""
            card_dsct = f'💥 <b>Descuento TC:</b> %{i["card_dsct"]} {card_d}\n' if i["card_dsct"] != 0 else ""
            web_dsct = f'💵 <b>Descuento web:</b> %{i["web_dsct"]} {web_d}\n' if i["web_dsct"] != 0 else ""

            if any([list_price, best_price, card_price]):
                msn = (
                    "🌟🦙 <b>Detalles del Producto</b> 🦙🌟\n\n"
                    f'{i["image"]}\n'
                    f'✅ <b>Marca:</b> {i["brand"]}\n'
                    f'📦 <b>Producto:</b> {i["product"]}\n\n'
                    f'{list_price}{best_price}{card_price}\n'
                    f'{card_dsct}{web_dsct}'
                    f'🏬 <b>Link:</b> {i["link"]}'
                )

                url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&parse_mode=HTML&text={msn}"
                response = requests.get(url)
                print(response)


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

