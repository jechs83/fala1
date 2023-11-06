import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import sys
from datetime import datetime
from bd_record import save_data_to_mongo_db
import pytz
import random
import time
import json
import re
from datetime import datetime
from datetime import date
from decouple import config
text_file = open(config("PROXY"), "r")
lines = text_file.readlines() 


web_url = random.choice(lines)
client = MongoClient(config("MONGO_DB"))

def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now

def consultar_mongodb():
    # Configura la conexión a la base de datos MongoDB

    db = client["brand_allowed"]
    collection = db["todo"]

    # Consulta la base de datos para verificar si la marca está permitida
    results = collection.find()

    # Crea una lista con los documentos encontrados
    brand_list = [doc["brand"] for doc in results]

    # Cierra la conexión a MongoDB
 

    return brand_list


brand = "samsung"


for i in range(100):
    if brand not in consultar_mongodb():
        print("no esta en la lista ")
        continue
    else:
        print("si esta en la lista")    




    
