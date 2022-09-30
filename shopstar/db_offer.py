import sys
sys.path.append('/Users/javier/GIT/fala') 
import time
import requests
from pymongo import MongoClient
import re
from datetime import datetime
from wong.g_var import mongo_db
mensaje = "Mensaje de prueba"
date = datetime.today().strftime('%d-%m-%Y')
date_now = datetime.today().strftime('%d-%m-%Y')



def tele_msm(message):
    requests.post("https://api.telegram.org/bot5504401191:AAG8Wuk5AF95qEWn0642ZjhzduE0CbVkBaU/sendMessage",
                
    data= {'chat_id': '-1001765171182','text': str(message)  }  )
    
    
def filtro_shopstar():
  
    client = MongoClient(mongo_db)

            
    db = client["shopstar"]
    collection = db["shop"] 

    x = collection.find({"card_dsct": {"$gte": 50},"brand": {"$in":
                        [ re.compile("samsung", re.IGNORECASE), re.compile("lg", re.IGNORECASE), re.compile("lenovo", re.IGNORECASE), 
                            re.compile("sony", re.IGNORECASE), re.compile("tcl", re.IGNORECASE), re.compile("hisense", re.IGNORECASE), re.compile("panasonic", re.IGNORECASE), 
                                re.compile("mabe", re.IGNORECASE), re.compile("bosch", re.IGNORECASE), re.compile("asus", re.IGNORECASE), re.compile("acer", re.IGNORECASE), 
                                    re.compile("apple", re.IGNORECASE), re.compile("xiaomi", re.IGNORECASE), re.compile("huawei", re.IGNORECASE), re.compile("hp", re.IGNORECASE), 
                                        re.compile("motorola", re.IGNORECASE), re.compile("aiwa", re.IGNORECASE), re.compile("toshiba", re.IGNORECASE), re.compile("adata", re.IGNORECASE), 
                                        re.compile("indurama", re.IGNORECASE), re.compile("oster", re.IGNORECASE), re.compile("karcher", re.IGNORECASE), re.compile("epson", re.IGNORECASE), 
                                        re.compile("canon", re.IGNORECASE)]}})
    


    db = client["shopstar"]
    collection1 = db["offers"] 



    array=[]
    for i in (x) :

        data = [i["_id"],i["brand"],i["product"],i["sku"],
        i["list_price"],i["best_price"],i["card_price"],i["web_dsct"],i["card_dsct"],
        i["link"],i["image"],i["date"]]



        array.append(data)
    #print(array)

    for i,v in enumerate(array):
        print(v)
        y = collection1.find_one({"_id":v[0]})
        if y:
            filter = {"_id":v[0]}
            newvalues = {"$set":{     

            "_id":v[0],
            "brand":v[1],
            "product":v[2],
            "sku":v[3],      
            "list_price":v[4],
            "best_price":v[5],
            "card_price":v[6],
            "web_dsct":v[7],
            "card_dsct":v[8],
            "link":v[9],
            "image":v[10],
            "date":v[11]

            }}
            collection1.update_one(filter, newvalues)     

        else:
            data={

            "_id":v[0],
            "brand":v[1],
            "product":v[2],
            "sku":v[3],      
            "list_price":v[4],
            "best_price":v[5],
            "card_price":v[6],
            "web_dsct":v[7],
            "card_dsct":v[8],
            "link":v[9],
            "image":v[10],
            "date":v[11]


            }
            collection1.insert_one(data) 

filtro_shopstar()