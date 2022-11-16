import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime
import random
import time
import json
import re
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

web="https://platanitos.com/catalogo?breadcrumbs[]=Tel%C3%A9fonos+m%C3%B3viles+y+accesorios&sort=timestamp_active+desc"
def scrap (web):


    proxies = {"http":"http://"+web_url }
        
    res=requests.get(web,  proxies= proxies)
    print("Respuesta del servidor :"+str(res.status_code))



    soup = BeautifulSoup(res.text, "html.parser")
        
    script_text = soup.find("script", text=re.compile("dataLayer.push")).text.replace("dataLayer.push(","[").replace(");","]")
    script_text = script_text.replace("'",'"')

  
    
 
    data =json.loads(script_text) 
    print(data)
    for idx, producto in enumerate(data[0]["ecommerce"]["impressions"]):
        print(producto["name"])

    
scrap(web)