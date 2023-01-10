
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import sys
from datetime import datetime
import pytz
import random
import time
from bd_record import save_data_to_mongo_db
from decouple import config
from datetime import datetime
from datetime import date

web_url = random.choice(config("PROXY"))
client = MongoClient(config("MONGO_DB"))

def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now

first_sku = None

def scrap (web):
    global first_sku
    proxies = {"http":"http://"+web_url }
        
    print(web_url)
    print("#####################################################################################")
    res=requests.get(web,  proxies= proxies)
    print("Respuesta del servidor :"+str(res.status_code))

    soup = BeautifulSoup(res.text, "html.parser")

    if res.status_code == 404:
        return False

i = 1

while i == 1:

    scrap("https://queue.teleticket.com.pe/?c=puntoticket&e=emp009&cid=es-CL&t_cal=1&t_ct=3")
   