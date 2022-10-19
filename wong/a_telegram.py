#https://api.telegram.org/
#https://core.telegram.org/bots/api
import sys
import time
import requests
from pymongo import MongoClient
import os
import ast
from datetime import datetime
import re
from telegram import ParseMode
from g_var import mongo_db
date = datetime.today().strftime('%d/%m/%Y')
date_now = datetime.today().strftime('%d/%m/%Y')

mensaje = ""


def send_telegram(message):
    requests.post("https://api.telegram.org/bot5504401191:AAG8Wuk5AF95qEWn0642ZjhzduE0CbVkBaU/sendMessage",
                
    # ENTER PRISE data= {'chat_id': '-1001765171182','text': str(message) , 'parse_mode':ParseMode.HTML}  )
    data= {'chat_id': '-1001811194463','text': str(message) , 'parse_mode':ParseMode.HTML}  ) # DISC0VERY
 

client = MongoClient(mongo_db)

db = client["cencosud"]
collection = db["market"] 

## QUERYS DE MONGO PARA BUSCAR OFERTAS O PRECIOS BUGS 
t1 = collection.find({   "description":{"$regex" : '55"' }, "best_price":{"$lte":1000, "$ne":0}    })
t2 = collection.find({   "description":{"$regex" : '50"' }, "best_price":{"$lte":1000, "$ne":0}  })
t3 = collection.find({   "description":{"$regex" : '65"' }, "best_price":{"$lte":1000, "$ne":0}  })
t4 = collection.find({ "description":{"$regex":'70"'}, "best_price":{"$lte":1500, "$ne":0}  })
t5 = collection.find({ "description":{"$regex":'75"'}, "best_price":{"$lte":1500, "$ne":0}  })
t6 = collection.find({   "description":{"$regex" :'lavadora',"$options":"i"}, "best_price":{"$lte":700, "$ne":0}  })
t7 =collection.find({"description":{"$regex" :'refrigeradora',"$options":"i"}, "best_price":{"$lte":1000, "$ne":0}})
t8 = collection.find({   "description":{"$regex" :'ryzen',"$options":"i"}, "best_price":{"$lte":1300, "$ne":0}, "category":{"$regex":"laptop","$options":"i" } })
t9 = collection.find({   "description":{"$regex" :'i7',"$options":"i"}, "best_price":{"$lte":1300, "$ne":0}, "category":{"$regex":"laptop","$options":"i" } })
t10 = collection.find({   "description":{"$regex" :'i5',"$options":"i"}, "best_price":{"$lte":1300, "$ne":0}, "category":{"$regex":"laptop","$options":"i" } })
t11 = collection.find({   "description":{"$regex" :'i3',"$options":"i"}, "best_price":{"$lte":1300, "$ne":0}, "category":{"$regex":"laptop","$options":"i" } })
t12 = collection.find({ "description":{"$regex" :"aspiradora","$options":"i"}, "best_price":{"$lte":200, "$ne":0}    })
t13 = collection.find({ "description":{"$regex" :"secadora","$options":"i"}, "best_price":{"$lte":400, "$ne":0}    })
t14 = collection.find( {"dsct":{"$gte":10}, "brand":{"$in":["nex.*", "lenovo.*" ]}})
t15 =  collection.find( {"dsct":{"$gte":70},"brand":{"$in":[ 
    re.compile("samsung", re.IGNORECASE),re.compile("lenovo", re.IGNORECASE),re.compile("sony", re.IGNORECASE),
    re.compile("lg", re.IGNORECASE),re.compile("asus", re.IGNORECASE),re.compile("xiaomi", re.IGNORECASE),
    re.compile("indurama", re.IGNORECASE),re.compile("oster", re.IGNORECASE),re.compile("bosch", re.IGNORECASE),
    re.compile("acer", re.IGNORECASE),re.compile("huawei", re.IGNORECASE),re.compile("panasonic", re.IGNORECASE),
    re.compile("winia", re.IGNORECASE),re.compile("phillips", re.IGNORECASE),re.compile("mabe", re.IGNORECASE),
    re.compile("nex", re.IGNORECASE)
                                   
     ]}})

pro = [t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15]  ## ARREGLO DE LOS QUERYS DE MONGO PARA MANDAR POR TELEGRAM
products = []

## FUNCION QUE COLOCA EN UNA LISTA (products) TODO LOS PRODUCTOS PARA SER MANDADOS A TELEGRAM,
## AQUI SE LE PASA EL OBJETO  MONGO PARA ITERACION Y EXTRACCIONDE LOS CAMPOS
def mongodb_search():
    for idx, value in enumerate(pro):
        for i in value:
            mongo_obj = [   i["image"], i["brand"] , i["description"], i["list_price"], 
                            i["best_price"], i["card_price"], i["link"]  
                        ]
            #print(val)
            products.append(mongo_obj)
            time.sleep(2)
    #print(products)
    
    
## ESTA FUNCION ITERA LOS OBJETOS QUERY EN LA FUNCION MONGODB_SEARCH Y FILTRA LOS MENSAJES REPETIDOS
## Y MANDA  SI HAY PRODUCTOS NUEVOS O SI SON REPETIDOS NO MANDA NADA
#########################################################################################

def auto_telegram():
   mongodb_search()
   for i,v in enumerate(products):
       send_telegram ("<b>Marca: "+v[1]+"</b>\nModelo: "+v[2]+"\nPrecio Lista :"+str(v[3])+"\n<b>Precio web :"+str(v[4])+"</b>\nPrecio Tarjeta :"+str(v[5])+"\n"+v[0]+"\nLink :"+str(v[6]))








