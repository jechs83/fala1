import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import sys
from datetime import datetime
import random
import gc
import time
import json
from bd_record import save_data_to_mongo_db
from datetime import datetime
from datetime import date
from multiprocessing import Pool, freeze_support
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

HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}


def shop(web):

    proxies = {"http":"http://"+web_url }
    res=requests.get(web,  proxies= proxies)
    print(res.status_code)
    soup = BeautifulSoup(res.text, "html.parser")

    elements=soup.find_all("div", class_="item-product product-listado")
    if not elements:
        return True
    
    for idx, i in enumerate(elements):
    
        try:
            link=i.find("a", class_="prod-det-enlace").attrs.get("href")
        except: link = None

        try:
            brand=i.find("div" ,class_="brand js-brand").text
        except: brand = "Null"

        try:
            best_price=i.find("div").attrs.get("data-best-price")
            best_price = best_price.replace("S/ ","").replace(",","").replace("S/. ","")
        except: best_price=0
            
        try:
            list_price=i.find("div").attrs.get("data-list-price")
            list_price = list_price.replace("S/ ","").replace(",","").replace("S/. ","")
        except: list_price = 0

        try:
            sku=i.find("div").attrs.get("data-id")
        except: sku = 0

        try:
            category=i.find("div").attrs.get("data-category")
        except: category = None

        try:
            product=i.find( "input" ,class_="insert-sku-quantity").attrs.get("title")
        except: product = None

        try:
            image=i.find( "img").attrs.get("src")
        except: image = None

        try:
         if best_price ==0 and list_price==0 or best_price == list_price:
            web_dsct=0
         else:
            web_dsct= float(list_price)-float(best_price)
            web_dsct = float(web_dsct)*100/float(list_price)
            web_dsct=round(web_dsct,2)
        except:web_dsct = 0

        bd_name_store = "promart"
        collection = "market"
        market = "promart"
        card_price = 0
        card_dsct =0
        dsct = web_dsct
        date_time = load_datetime()
        print(),print(brand),print(sku),print(product) ,print(link),print(category),print(list_price)
        print(best_price),print(image),print(market),print(web_dsct)

        save_data_to_mongo_db(bd_name_store,collection, market,sku,brand,product,list_price,
                            best_price,card_price,link,image,dsct, card_dsct, date_time[0] ,date_time[1],web)


num = sys.argv[1]
#arg_ = r"C:\\GIT\\fala\\falabella\\urls\\test\\url"+str(num)+".txt"
arg_ = r"/Users/javier/GIT/fala/promart/urls/link"+str(num)+".txt"
array_tec = []

f = open(arg_, "r")
x = f.readlines()
for i in x:
    #array_tec.append(i.rstrip()) 
    array_tec.append(i.split()) 
        


lista = []
inicio = None
for i,v  in enumerate  (array_tec):
    if i ==0:
        inicio = load_datetime()
    for i in range (200):
        lista.append(v[0]+str(i+1))


    if __name__ == '__main__':

            freeze_support()
            p = Pool()
            p.map (shop,lista)
            p.terminate()
            p.join()
        

print(inicio)
print(load_datetime())


# inicio =None
# for i in range (15):
#     if i == 0:
#      inicio = load_datetime()
#     web = "https://simple.ripley.com.pe/tecnologia/celulares/celulares-y-smartphones?page="+(str(i+1))

#     scrap(web)


# print(inicio)
# print(load_datetime())






    