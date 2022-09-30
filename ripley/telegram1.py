import sys
import time
import requests
from pymongo import MongoClient
import os
import ast
import re
from datetime import datetime
from g_var import mongo_db
from telegram import ParseMode
date = datetime.today().strftime('%d/%m/%Y')
date_now = datetime.today().strftime('%d/%m/%Y')
print(date_now)

mensaje = "test message"

def send_telegram(message):
    requests.post("https://api.telegram.org/bot5504401191:AAG8Wuk5AF95qEWn0642ZjhzduE0CbVkBaU/sendMessage",
            
    data= {'chat_id': '-1001765171182','text': str(message) , 'parse_mode':ParseMode.HTML}  )


client = MongoClient(mongo_db)
db = client["ripley"]
collection = db["market"] 

## QUERYS DE MONGO PARA BUSCAR OFERTAS O PRECIOS BUGS 
t1 = collection.find( {" date ": date_now, "web_dsct" : { "$gte" : 80 } })
t2 = collection.find( {" date ": date_now, "web_dsct" : { "$gte" : 70 } })
# t2 = collection.find({   "product":{"$regex" : '50"' },"date":date_now, "best_price":{"$lte":1000, "$ne":0}  })
# t3 = collection.find({   "product":{"$regex" : '65"' }, "date":date_now,"best_price":{"$lte":1000, "$ne":0}  })
# t4 = collection.find({ "product":{"$regex":'70"'}, "date":date_now,"best_price":{"$lte":1500, "$ne":0}  })
# t5 = collection.find({ "product":{"$regex":'75"'},"date":date_now, "best_price":{"$lte":1500, "$ne":0}  })
# t6 = collection.find({   "product":{"$regex" :'lavadora',"$options":"i"}, "date":date_now,"best_price":{"$lte":1000, "$ne":0}, "brand":{"$regex":"samsung","$options":"i"}, "brand":{"$regex" :'lg',"$options":"i"} })
# t7= collection.find( {"best_price":{"$lte":1000},"date":date_now,"brand":{"$in":[ 
#                         re.compile("samsung", re.IGNORECASE),re.compile("lg", re.IGNORECASE),re.compile("indurama", re.IGNORECASE),
#                         re.compile("bosch", re.IGNORECASE),re.compile("panasonic", re.IGNORECASE),re.compile("mabe", re.IGNORECASE)]}})
# #t14 = collection.find( {"dsct":{"$gte":10}, "brand":{"$in":["nex.*", "lenovo.*" ]}})
# t8 =  collection.find( {"web_dsct":{"$gte":90},"date":date_now,"brand":{"$in":[ 
#     re.compile("samsung", re.IGNORECASE),re.compile("lenovo", re.IGNORECASE),re.compile("sony", re.IGNORECASE),
#     re.compile("lg", re.IGNORECASE),re.compile("asus", re.IGNORECASE),re.compile("xiaomi", re.IGNORECASE),
#     re.compile("indurama", re.IGNORECASE),re.compile("oster", re.IGNORECASE),re.compile("bosch", re.IGNORECASE),
#     re.compile("acer", re.IGNORECASE),re.compile("huawei", re.IGNORECASE),re.compile("panasonic", re.IGNORECASE),
#     re.compile("winia", re.IGNORECASE),re.compile("phillips", re.IGNORECASE),re.compile("mabe", re.IGNORECASE)
                                   
#      ]}})

pro = [t1,t2]  ## ARREGLO DE LOS QUERYS DE MONGO PARA MANDAR POR TELEGRAM
products = []

# FUNCION QUE COLOCA EN UNA LISTA (products) TODO LOS PRODUCTOS PARA SER MANDADOS A TELEGRAM,
# AQUI SE LE PASA EL OBJETO  MONGO PARA ITERACION Y EXTRACCIONDE LOS CAMPOS
def mongodb_search():
    for idx, value in enumerate(pro):
    
        for i in value:
            mongo_obj = [   
                            i["_id"],
                            i["brand"],
                            i["product"],
                            i["list_price"],
                            i["best_price"],
                            i["card_price"],
                            i["image"],
                            i["link"],
                            i["web_dsct"],
                        ]
            #print(val)
            products.append(mongo_obj)


# for idx
# send_telegram ("<b>Marca: "+i["brand"]+"</b>\nModelo: "+i["product"]+"\nPrecio Lista :"+str(i["list_price"])+"\n<b>Precio web :"+str(i["best_price"])+"</b>\nPrecio Tarjeta :"+"\n"+i["image"]+"\n\nLink :"+i["link"])

    
