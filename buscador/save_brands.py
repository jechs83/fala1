import sys
import time
import requests
from pymongo import MongoClient
import os
import pymongo
import re
from bd_compare import save_data_to_mongo_db
from decouple import config
from datetime import datetime
from telegram import ParseMode
import pytz
server_date = datetime.now()
timezone = pytz.timezone("America/Bogota")
peru_date = server_date.astimezone(timezone)
date = peru_date.strftime("%d/%m/%Y" )

#https://api.telegram.org/bot5573005249:AAFGCjc7zuI1XoHMqbd6gr1I1ZVi9Xd2I9s/sendMessage

def send_telegram(message, bot_tokey_key, chat_ide):
    requests.post("https://api.telegram.org/bot"+str(bot_tokey_key)+"/sendMessage",
            
    data= {'chat_id': chat_ide ,'text': str(message) , 'parse_mode':ParseMode.HTML}  ) # DISC0VERY
    

client = MongoClient(config("MONGO_DB"))
db5 = client["scrap"]
collection5 = db5["scrap"] 


def save_brand_to_mongodb(brand,category):

        db = client["brands"]
        collection= db[category]

        x = collection.find_one({"brand":brand})
      
        if x  :
            #print(" ACTUALIZA BASE DE DATOS ")
            filter = {"brand":brand}
            newvalues = { "$set":{ 
            "brand":brand}   
           
            }
            collection.update_one(filter,newvalues)            
        else:
            
            data =  {
            "brand":brand     

            }
            collection.insert_one(data)



def brand_list(brand,category):

    db = client["brands"]
    collection= db[category]
    t9 = collection.find({})

    for i in t9:
        print(i)
        print("se envio lista ropa")      
        save_brand_to_mongodb(brand,category)



with open ("/Users/javier/GIT/fala/buscador/ropa.txt","r" ) as brands:
    x = brands.readlines()

for i in x:
    brand = i.replace("\n","")
    save_brand_to_mongodb(brand,"ropa")
    
