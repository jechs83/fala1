import time
import requests
import sys
sys.path.append('/Users/javier/GIT/fala') 
import sys
import os
from wong.g_var import mongo_db
from pymongo import MongoClient
import re



mensaje = "Mensaje de prueba"


def tele_msm(message):
    requests.post("https://api.telegram.org/bot5504401191:AAG8Wuk5AF95qEWn0642ZjhzduE0CbVkBaU/sendMessage",
                
    data= {'chat_id': '-1001765171182','text': str(message)  }  )
    
    
def filtro_promart():

  client = MongoClient(mongo_db)
          
  db = client["shopstar"]
  collection = db["market"] 

  x = collection.find({"card_dsct": {"$gte": 60}})
    
  db = client["shopstar"]
  collection1 = db["offers"] 

  array=[]
  for i in (x) :

      data = [
              i["_id"],i["brand"],
              i["product"],i["market"],i["sku"],
              i["list_price"],i["best_price"],i["card_price"],i["web_dsct"],i["card_dsct"],
              i["seller"],i["link"],i["image"],i["date"]
             ]
      array.append(data)
  print(array)

  '''for i,v in enumerate(array):
        y = collection1.find_one({"_id":v[0]})
        if y:
          filter = {"_id":v[0]}
          newvalues = {"$set":{     

          "_id":v[0],
          "brand":v[1],
          "product":v[2],
          "market":v[3],
          "sku":v[4],
          "list_price":v[5],
          "best_price":v[6],
          "card_price":v[7],
          "web_dsct":v[8],
          "card_dsct":v[9],
          "seller":v[10],
          "link":v[11],
          "image":v[12],
          "date":v[13]

            }}
          collection1.update_one(filter, newvalues)     

        else:
          data={

          "_id":v[0],
          "brand":v[1],
          "product":v[2],
          "market":v[3],
          "sku":v[4],
          "list_price":v[5],
          "web_price":v[6],
          "card_price":v[7],
          "web_dsct":v[8],
          "card_dsct":v[9],
          "seller":v[10],
          "link":v[11],
          "image":v[12],
          "date":v[13]


            }
          collection1.insert_one(data) '''

filtro_promart()

