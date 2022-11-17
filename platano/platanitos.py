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


web_url = random.choice(config("PROXY"))
client = MongoClient(config("MONGO_DB"))

def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now

firstProduct = None
def scrap (web):

    global firstProduct
    proxies = {"http":"http://"+web_url }
        
    res=requests.get(web,  proxies= proxies)
    print("Respuesta del servidor :"+str(res.status_code))



    soup = BeautifulSoup(res.text, "html.parser")


    #data = soup.find("div", class_="col-12 d-none d-lg-block")
    data = soup.find_all("div", class_="col-flt col-3")


    try:

     no_page = soup.find("h3", class_="nosearch-title mb-3").text
    except: no_page = True
    if no_page == "No encontramos resultados que coincidan con tu búsqueda":
            return False
    print(no_page)
    for idx, producto in enumerate (data):
          
        try:
         product = producto.find("p", class_="nd-ct__item-title line-clamp-2").text
        except: product = None
       
        if idx == 0:
            if firstProduct == product:
                return False
            
            firstProduct = product

    

        try:
         dsct = producto.find("div", class_="nd-ct__label-porc ps-1 pe-1 me-2").text

         dsct = dsct.replace("-","").replace("%","")
        except: dsct = 0

        

        try:
         brand = producto.find("p", class_="nd-ct__item-title line-clamp-2").text
         brand = brand.split()
         brand = brand[0]
        except: brand = None

   

        try:
         list_price = producto.find("p", class_="nd-ct__item-prices").text
         list_price = list_price.split()
         list_price = list_price[3]
        except: list_price = 0

        try:
         best_price = producto.find("p", class_="nd-ct__item-prices").text
         best_price = best_price.split()
         best_price = best_price[1]
        except: best_price = 0

        try:
         image = producto.find("img").attrs.get("src")
        except: image = None

        try:
         link = producto.find("a").attrs.get("href")
         link = "https://platanitos.com"+link
        except: link = None

        sku  = product.replace(" ","")




        # print()
        # print(idx+1)
        # print(brand)
        # print(product)
        # print(list_price)
        # print(best_price)
        # print(image)
        # print(link)
        # print(sku)

        # print(dsct)

        bd_name_store = "platanitos"
        collection = "market"  #   NOMBRE DE BASE DE DATOS
        market = "platanitos"    # COLECCION
        card_price = 0
        card_dsct = 0
        date_time = load_datetime()
        try:
         save_data_to_mongo_db(bd_name_store,collection, market,sku,brand,product,list_price,
                            best_price,card_price,link,image,dsct, card_dsct, date_time[0] ,date_time[1])

        except:
            continue
    



array_tec=[]

#arg_ = sys.argv[1]
num = sys.argv[1]
arg_ = config("PLATANITOS_TEXT_PATH")+str(num)+".txt"

f = open(arg_, "r")
x = f.readlines()

for i in x:
    array_tec.append(i.rstrip()) 

print(array_tec)

count = len(array_tec)

def platanito_scrapper():
    page = -100
    for id, val in enumerate(array_tec):
                                                                                                                                                                                                                                                                                      
        for i in range (200) : 

            page = page+100  

            if val[-4:]=="desc":
                url = val  
            if val[-1:]   == "=" :
                url =    val+str(page)                                                                                                                                                                                                                                                                      
            
            print(url)
            succes = scrap(url) ## GENERA LA LISTA DE PAGINACIONES POR CATEGORIA
            if succes == False:
                break

       

        if id == count-1:
            print("se acabo la web y va comenzar a dar vueltas")
            time.sleep(10)
            
            platanito_scrapper() 
        



platanito_scrapper()








    