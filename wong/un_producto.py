import sys
import time
import requests
from pymongo import MongoClient
import os
import ast
import re
from datetime import datetime
from telegram import ParseMode
from g_var import mongo_db

date = datetime.today().strftime('%d/%m/%Y')
date_now = datetime.today().strftime('%d/%m/%Y')

mensaje = "test message"

def send_telegram(message):
    requests.post("https://api.telegram.org/bot5504401191:AAG8Wuk5AF95qEWn0642ZjhzduE0CbVkBaU/sendMessage",
            
    # ENTER PRISE data= {'chat_id': '-1001765171182','text': str(message) , 'parse_mode':ParseMode.HTML}  )
    data= {'chat_id': '-1001811194463','text': str(message) , 'parse_mode':ParseMode.HTML}  ) # DISC0VERY


client = MongoClient(mongo_db)


#arg_sku = sys.argv[1]
        
db = client["cencosud"]
collection = db["market"] 


## QUERYS DE MONGO PARA BUSCAR OFERTAS O PRECIOS BUGS 
t1 = collection.find({"sku":39213975})

for i in t1:
   print(i)
   print("pasa por aqui")
   
   send_telegram ("<b>Marca: "+i["brand"]+"</b>\nModelo: "+i["product"]+"\nPrecio Lista :"+str(i["list_price"])+"\n<b>Precio web :"+str(i["best_price"])+"</b>\nPrecio Tarjeta :"+"\n"+i["image"]+"\n\nLink :"+i["link"])

  
# pro = t1  ## ARREGLO DE LOS QUERYS DE MONGO PARA MANDAR POR TELEGRAM
# products = []

# print()

# ## FUNCION QUE COLOCA EN UNA LISTA (products) TODO LOS PRODUCTOS PARA SER MANDADOS A TELEGRAM,
# ## AQUI SE LE PASA EL OBJETO  MONGO PARA ITERACION Y EXTRACCIONDE LOS CAMPOS
# def mongodb_search():
#     for idx, value in enumerate(t1):

#         print(value)
#         for i in value:
         
#             mongo_obj = [   i[0], i[1] , i[2]#, i["list_price"], 
#                             # i["best_price"], i["card_price"], i["link"] ,i["web_dsct"],i["sku"]
#                         ]

#             #print(val)
#             products.append(mongo_obj)
#             time.sleep(2)
#     print()
#     print(type(products))
#     c = ast.literal_eval(products)
#     print(c[3])
  

# ## ESTA FUNCION ITERA LOS OBJETOS QUERY EN LA FUNCION MONGODB_SEARCH Y FILTRA LOS MENSAJES REPETIDOS
# ## Y MANDA  SI HAY PRODUCTOS NUEVOS O SI SON REPETIDOS NO MANDA NADA
# #########################################################################################
# mongodb_search()
#send_telegram ("<b>Marca: "+products[1]+"</b>\nModelo: "+products[2]+"\nPrecio Lista :"+products[3]+"\n<b>Precio web :"+products[4]+"</b>\nPrecio Tarjeta :"+products[5]+"\n"+products[0]+"\nLink :"+products[6])
#send_telegram ("<b>Marca: "+products[1])

          
