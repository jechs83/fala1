import sys
import time
import requests
from pymongo import MongoClient
import os
import pymongo
import ast

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



def send_telegram(message):
    requests.post(config("ENTERPRISE_KEY"),
            
    data= {'chat_id': '-819583862','text': str(message) , 'parse_mode':ParseMode.HTML}  ) # DISC0VERY
    

client = MongoClient(config("MONGO_DB"))
db5 = client["scrap"]
collection5 = db5["scrap"] 
collection_offer1 = db5["offer1"]
collection_offer2 = db5["offer2"]






b = collection_offer1.find({"_id":"804515"})
b = list(b)
print(len(b))
for i in b:
    try:
        print(i)
    except:
        print("no hay ")

    print(type(i))



