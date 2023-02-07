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


def scrap (web):
 
    proxies = {"http":"http://"+web_url }
    res=requests.get(web,  proxies= proxies, headers= HEADERS)
    print("Respuesta del servidor :"+str(res.status_code))
    soup = BeautifulSoup(res.text, "html.parser")
    
    error = soup.find( "h3" , class_="jsx-860724461")

    if error:
        return False
    try:
     data = soup.find("script", id="__NEXT_DATA__" ).text
    except: return False

    js = json.loads(data)
    try:
     x = js["props"]["pageProps"]["results"]
    except: return False

    for i in range (55):

        try:
            brand = x[i]["brand"]
        except: brand= "None"

        try:
            product = x[i]["displayName"]
        except: product= "None"

        try:
            web_dsct = x[i]["discountBadge"]["label"]
            web_dsct = web_dsct.replace("-","").replace("%","")
        except: web_dsct =0

        if web_dsct ==0:
            continue

        try:
            image = x[i]["mediaUrls"][0]
        except:  
            try:    
                image = x[i]["mediaUrls"]
            except: image = "None"

        try:
            sku = x[i]["skuId"]
        except: sku = 0

        if sku ==0:
            continue

        try:
            link = x[i]["url"]
        except: link = "None"

        try:
            card_price = x[i]["prices"][0]["price"][0]
            card_price = card_price.replace(",","")
        except: card_price = 0

        try:
            best_price = x[i]["prices"][1]["price"][0]
            best_price = best_price.replace(",","")
        except: best_price= 0

        try:
            list_price= x[i]["prices"][2]["price"][0]
            list_price = list_price.replace(",","")
        except: list_price = 0 

      
        print()
        print( "producto numero "+ str(i+1));
        print(sku);print(brand);print(product);print("list price "+str(list_price));print("best price "+str(best_price));print("card price "+str(card_price));
        print("descuento "+str(web_dsct)); print("link "+link)
        

        bd_name_store = "saga"
        collection = "market"  #   NOMBRE DE BASE DE DATOS
        market = "saga"    # COLECCION
        dsct = web_dsct
        card_dsct = 0
        date_time = load_datetime()

        save_data_to_mongo_db(bd_name_store,collection, market,sku,brand,product,list_price,
                             best_price,card_price,link,image,dsct, card_dsct, date_time[0] ,date_time[1],web)


num = sys.argv[1]
#arg_ = r"C:\\GIT\\fala\\falabella\\urls\\test\\url"+str(num)+".txt"
arg_ = r"/Users/javier/GIT/fala/falabella/urls/test/url"+str(num)+".txt"
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
    for i in range (int(v[1])):
        lista.append(v[0]+str(i+1))


    if __name__ == '__main__':

            freeze_support()
            p = Pool()
            p.map (scrap,lista)
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






    