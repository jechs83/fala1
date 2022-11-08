import sys
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime

import os
import json
import random
from datetime import date
import json
import time

current_time= time.strftime("%H:%M")
date = date.today()
current_day= date.strftime("%d/%m/%Y")
from decouple import config
web_url = random.choice(config("PROXY"))
client = MongoClient(config("MONGO_DB"))


first_product = None
def scrap (web):
    global first_product
    proxies = {"http":"http://"+web_url }
        
    res=requests.get(web,  proxies= proxies)
    print("Respuesta del servidor :"+str(res.status_code))

   
    res=requests.get(web,  proxies= proxies)
    soup = BeautifulSoup(res.text, "html.parser")

    element = soup.find("div", "products")

    count = 0
    db = client["cahema"]
    collection = db["market"]
    db2 = client["scrap"]
    collection2 = db2["scrap"]
    market = "cahema"

    for i in element:
        count= count+1
        # with open("/Users/javier/GIT/fala/cahema/source.txt", "w" ) as f:
        #     f.write(str(i))

        product = i.find("a").text
      
        print(product)
        
        
        # if product == first_product:
        #     print("se repite la pagina")
        #     return False
        # if count == 1:
        #     first_product = product

        # try:
        #  gray = i.find("div", "product-thumbnail graypicture")
        # except: print("existe producto")
        # if gray:
        #     continue

        # try:
        #  best_price = i.find("span", class_="price").text
        # except: best_price = 0
        # best_price=str(best_price)
        # best_price = best_price.replace("S/.","").replace(",","")

        # link = i.find("a", class_="product-thumbnail-link").attrs.get("href")
        # try:
        #  image = i.find("img").attrs.get("src")
        # except: image = None
        # try:
        #  list_price = i.find("span", class_="regular-price").text
        # except: list_price  = 0
        # list_price = str(list_price)
        # list_price = list_price.replace("S/.","").replace(",","")
        # try:
        #  dsct = i.find("span", class_="discount-percentage discount-product").text
        #  dsct = dsct.replace("-","").replace("%","")
        # except: dsct = 0

        # print()
        # print(link)
        # print(image)
        # print(product)
        # print(list_price)
        # print(best_price)
        # print(dsct)
        # category = None
        # brand = "cahema"
        # sku= product.replace(" ","")
        

        # # y = collection.find_one({"id_": sku})
        # # z = collection2.find_one({"id_": sku})

        # y = collection.find_one({"produt": product})
        # z = collection2.find_one({"produt": product})

        # if y :
            
        #     filter = {"produt": product}
        #     newvalues = { "$set":{  
        #     #"id_":str(sku) ,
        #     "sku":str(sku), 
        #     "brand":brand,
        #     "product": product,
        #     "category":category,
        #     "list_price":float(list_price),
        #     "best_price":float(best_price),
        #     "card_price": 0,
        #     "web_dsct":float(dsct),
        #     "link": link,
        #     "image": image,
        #     "date":current_day,
        #     "market":market,
        #     "time":current_time
        #     }}
        #     collection.update_one(filter,newvalues)
               
        # else:
        #     #print("ADICIONA NUEVO REGISTRO A BD ")
            
            
        #     data =  {
        #     "id_":str(sku) ,
        #     "sku":str(sku), 
        #     "brand":brand,
        #     "product": product,
        #     "category":category,
        #     "list_price":float(list_price),
        #     "best_price":float(best_price),
        #      "card_price": 0,
        #     "web_dsct":float(dsct),
        #     "link": link,
        #     "image": image,
        #     "date":current_day,
        #     "market":market,
        #     "time":current_time
            
        #     }

        #     collection.insert_one(data)
            
       
       

        # if z :
            
        #     filter = {{"id_":sku} }
        #     newvalues = { "$set":{ 
        #     "id_":str(sku) ,
        #     "sku":str(sku), 
        #     "brand":brand,
        #     "product": product,
        #     "category":category,
        #     "list_price":float(list_price),
        #     "best_price":float(best_price),
        #     "card_price": 0,
        #     "web_dsct":float(dsct),
        #     "link": link,
        #     "image": image,
        #     "date":current_day,
        #     "market":market,
        #     "time":current_time
        #     }}
        #     collection2.update_one(filter,newvalues)
               
        # else:
        #     #print("ADICIONA NUEVO REGISTRO A BD ")
        #     data =  {
        #     "id_":str(sku) ,
        #     "sku":str(sku), 
        #     "brand":brand,
        #     "product": product,
        #     "category":category,
        #     "list_price":float(list_price),
        #     "best_price":float(best_price),
        #     "card_price": 0,
        #     "web_dsct":float(dsct),
        #     "link": link,
        #     "image": image,
        #     "date":current_day,
        #     "market":market,
        #     "time":current_time
        #     }

        #     collection2.insert_one(data)
            


scrap("https://cahema.pe/43-herramientas-inalambricas?page=1")