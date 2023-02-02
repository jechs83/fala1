
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
text_file = open(config("PROXY"), "r")
lines = text_file.readlines() 


prox = random.choice(lines)
print(prox)
client = MongoClient(config("MONGO_DB"))
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now

first_sku = None
HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

web = "https://www.tailoy.com.pe/electrohogar.html?p=1"
def scrap (web):
    global first_sku
    proxies = {"http":"http://"+prox }
    print(prox)
    res=requests.get(web,  proxies= proxies, headers=HEADERS)
    print("Respuesta del servidor :"+str(res.status_code))

    soup = BeautifulSoup(res.text, "html.parser")
  
    count=0
    
    productos = soup.find_all( "li", class_="item product product-item")


scrap(web)