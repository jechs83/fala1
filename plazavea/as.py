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
    res = requests.get(web, proxies = proxies).json()
    #print("Respuesta del servidor :"+str(res.status_code))

    for idx,i   in  enumerate (res):
        try:
            sku = i["productReference"]
        except:
            quit()
        product = i["productName"]
        brand = i["brand"]
        link= i["link"]
        image = i["items"][0]["images"][0]["imageUrl"]
        list_price = i["items"][0]["sellers"][0]["commertialOffer"]["ListPrice"]
        try:
            best_price=   i["items"][0]["sellers"][0]["commertialOffer"]["Price"]
        except:
            best_price = 0
        stock=  i["items"][0]["sellers"][0]["commertialOffer"]["IsAvailable"]
        try:
            dsct = (list_price*100/best_price)-100
        except:
            dsct = 0
        if dsct == 100:
            dsct = 0
        dsct = round(dsct)
        print()
        print(brand)
        print(product)
        print(sku)
        print(link)
        print(image)
        print(list_price)
        print(dsct)
        print(best_price)
        print(stock)

        bd_name_store = "plaza"
        collection = "market"  #   NOMBRE DE BASE DE DATOS
        market = "vea"    # COLECCION
        card_price = 0 
        card_dsct = 0

  
        
        date_time = load_datetime()
        save_data_to_mongo_db(bd_name_store,collection, market,sku,brand,product,list_price,
                            best_price,card_price,link,image,dsct, card_dsct, date_time[0] ,date_time[1],web)

       

num = sys.argv[1]
#arg_ = r"C:\\GIT\\fala\\falabella\\urls\\test\\url"+str(num)+".txt"
arg_ = r"/Users/javier/GIT/fala/plazavea/url/vea"+str(num)+".txt"
array_tec = []

f = open(arg_, "r")
x = f.readlines()
for i in x:
    #array_tec.append(i.rstrip()) 
    array_tec.append(i.split()) 
        


lista = []


# for i,v  in enumerate  (array_tec):
#     if i ==0:
#         inicio = load_datetime()
#     for i in range (int(v[1])):
#         lista.append(v[0]+str(i+1))

inicio = None
for i,web  in enumerate  (array_tec):
    if i ==0:
        inicio = load_datetime()
    for i in range (200):
        lista.append((web[0]+str(i*48)+web[1]+str((i+1)*48)))
       

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






    