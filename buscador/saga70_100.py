import logging
from telegram_search_engine import auto_telegram_between_values
from pymongo import MongoClient
from decouple import config

import time
import gc
from pymongo import MongoClient
import itertools
import re
import os
import requests
import time

from telegram_search_dbSave import save_data_to_mongo_db
from datetime import date
from decouple import config
from datetime import datetime
import pytz
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

mongo = "192.168.8.66:27017"
client = MongoClient(mongo)

# data_base = "saga"
# collection_db = "scrap"

bot_token =  "6664469425:AAFeuvjckKSK9sM0nsLCKbgGgJomAqXpGLA"
chat_id= "-1001811194463"


date_now = date.today().strftime("%d/%m/%Y")


#  ESTA FUNCION GUARDA EN LA BASE DE DATOS LOS PRODUCTOS SCRAPEADOS
def save_data_to_mongo_db( sku,brand,product,list_price,
                            best_price,card_price,link,image,dsct, card_dsct,data_base,collection_db):
        
        db = client[data_base]
        collection = db[collection_db]

        data = {
    
            "sku": sku,
            "brand": str(brand),
            "product": str(product),
            "list_price": float(list_price),
            "best_price": float(best_price),
            "card_price": float(card_price),
            "web_dsct": float(dsct),
            "card_dsct": float(card_dsct),
            "link": str(link),
            "image": str(image),
        }

        collection.update_one({"sku": sku}, {"$set": data}, upsert=True)
       

# ESTA FUNCION MANDA UN MENSAJE A TELEGRAM ( EL MENSAJE ES EL PRODUCTO EN OFERTA QUE SE LE PASA POR PARAMETRO)
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




def auto_telegram_between_values(  ship_db1,ship_db2, bot_token, chat_id,porcentage1, porcentage2,data_base, collection_db):

    print("buscando")
    db = client[data_base]
    collection = db[collection_db]
    collection_1 = db[ship_db1]
    collection_2 = db[ship_db2]

    ##########  OBTENGO LAS LISTAS DEL MONGO DE LOS PRODUCTOS CON EL RANGO DE DESCUENTO ##########
    scrap_search = collection.find({
        "$or": [
            {"web_dsct": {"$gte": porcentage1, "$lte": porcentage2}},
            {"card_dsct": {"$gte": porcentage1,  "$lte": porcentage2}},
        ],
        "date": date_now,
        # "product": {"$not": {"$in": [re.compile(producto, re.IGNORECASE), re.compile("reloj", re.IGNORECASE)]}}
            })
    #==================================================================================
    print("obtiene data de base principal")
    count = 0

    for i in scrap_search:
        count +=1

        data_live ={
               "sku": str(i["sku"]),
                "best_price":float(i["best_price"]),
                "list_price":float(i["list_price"]),
                "card_price":float(i["card_price"]),
                "web_dsct":float(i["web_dsct"]),
               "card_dsct": float(i["card_dsct"]),    
            }

        try:
            data_saved = collection_1.find_one({'sku': str(i['sku'])})
        
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
      
        print(data_sv)
   
        if data_live == data_sv:

            print("PRODUCTOS IGUALES, NO SE MANDA NADA A TELEGRAM Y NO DEBE GRABARSE TAMPOCO")
        
        if data_live != data_sv:

            if i["web_dsct"] <= 50 or i["card_dsct"] <= 50:
                web_d = "🟡"

            if (50 < i["web_dsct"] <= 69) or (50 < i["card_dsct"] <= 69):
                web_d = "🟢"

            if i["web_dsct"]  >=70 or  i["card_dsct"]  >=70:
                web_d = "🔥🔥🔥🔥🔥🔥🔥"
            
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
                        i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"], i["card_dsct"],data_base,ship_db1)
            
               

            send_telegram (msn,foto, bot_token, chat_id)

            print("LOS DATOS DEL PRODUCTO VARIO Y SE ENVIA A TELEGRAM ................................")
            print("###################################################################################")
         


        if data_live == data_sv:
            continue
    print("############      FIN     #############")
    gc.collect()



# def get_configuration(market,dsct):
#     return {
#         "mongo_db": config("MONGO_DB"),
#         "chat_id": "-1001811194463",
#         "bot_token": "6664469425:AAFeuvjckKSK9sM0nsLCKbgGgJomAqXpGLA",
#         "collection_name": config("collection"),
#         "bd_name": market,
#         "bd1": "bd1",
#         "bd2": "bd2",
#         "dsct": dsct,
#         "dsct2": 100,
#         "product": "reloj",
#         "db": "trigger",
#         "collection": "40"
#     }


def connect_to_mongo(mongo_db):
    try:
        client = MongoClient(mongo_db)
        logging.info("Connected to MongoDB")
        return client
    except Exception as e:
        logging.error(f"Failed to connect to MongoDB: {e}")
        raise

def buscador(market, dsct,bot_token, chat_id):
    client = MongoClient(mongo)
    db = client[market]
    collection = db["scrap"]

    while True:
        try:
            auto_telegram_between_values(
                "bd1",
                "bd2",
                bot_token,
                chat_id,
                dsct,
                100,
                market,
                "scrap"
            )
        except Exception as e:
            logging.error(f"An exception occurred: {e}")

# if __name__ == "__main__":
#     config = get_configuration()
#     try:
#         buscador(config)
#     except KeyboardInterrupt:
#         logging.info("Program interrupted by user")
#     except Exception as e:
#         logging.error(f"Unexpected error: {e}")


def main(market, dsct,bot_token, chat_id):
    
    try:
        buscador(market, dsct,bot_token, chat_id)
    except KeyboardInterrupt:
        logging.info("Program interrupted by user")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")



main("saga", 60,bot_token, chat_id)