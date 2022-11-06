import sys
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime

import os
import json
import random
from datetime import date

import time

current_time= time.strftime("%H:%M")
date = date.today()
current_day= date.strftime("%d/%m/%Y")
from decouple import config
web_url = random.choice(config("PROXY"))
client = MongoClient(config("MONGO_DB"))

web = "https://www.plazavea.com.pe/tecnologia/televisores?page=2"
def scrap (web):

    proxies = {"http":"http://"+web_url }
        
    res=requests.get(web,  proxies= proxies)
    print("Respuesta del servidor :"+str(res.status_code))

   
    res=requests.get(web,  proxies= proxies)
    soup = BeautifulSoup(res.text, "html.parser")

   


    try:
     elements = soup.find_all("div",class_="Showcase__content")
    except:
        return False

    for i in elements:
       
       
        print()
        try:
            product = i.find("figcaption").text
        except: product = 0
        print(product)

        try:
         brand = i.find("div", class_="Showcase__brand").text
        except: brand = None
        print(brand.strip())
        link = i.find("a", class_="Showcase__link").attrs.get("href")
        print(link)
        try:
            list_price = i.find("div", class_="Showcase__oldPrice").text
        except: list_price = 0
        list_price = str(list_price).replace("S/","").replace(",","")
        print(str(list_price).strip())


        try:
            best_price = i.find("div", class_="Showcase__salePrice").text
        except: best_price = 0
        best_price = best_price.replace("S/","").replace(",","")
        print(best_price.strip())
        
        try:
            image = i.find("figure", class_="Showcase__photo").find("img").attrs.get("src")
        except: image = None
        print(image)

        sku = product
    


        db = client["plazavea"]
        collection = db["market"]
        db2 = client["scrap1"]
        collection2 = db2["scrap1"]
        market = "vea"
        sku = None
        category = None
        dsct =None

        y = collection.find_one({"_id":market+str(sku)})
        z = collection2.find_one({"_id":market+str(sku)})

        if y :
            
            filter = {"_id":market+str(sku), }
            newvalues = { "$set":{ 
            "_id":market+str(sku),   
            "sku":str(sku), 
            "brand":brand,
            "product": product,
            "category":category,
            "list_price":float(list_price),
            "best_price":float(best_price),
            "card_price": 0,
            "web_dsct":float(dsct),
            "link": link,
            "image": image,
            "date":current_day,
            "market":market,
            "time":current_time
            }}
            collection.update_one(filter,newvalues)
               
        else:
            print("ADICIONA NUEVO REGISTRO A BD ")
            
            
            data =  {
            "_id":market+str(sku),   
            "sku":str(sku), 
            "brand":brand,
            "product": product,
            "category":category,
            "list_price":float(list_price),
            "best_price":float(best_price),
             "card_price": 0,
            "web_dsct":float(dsct),
            "link": link,
            "image": image,
            "date":current_day,
            "market":market,
            "time":current_time
            
            }

            collection.insert_one(data)
            
       
        y = collection2.find_one({"_id":market+str(sku)})

        if z :
            
            filter = {"_id":market+str(sku), }
            newvalues = { "$set":{ 
            "_id":market+str(sku),   
            "sku":str(sku), 
            "brand":brand,
            "product": product,
            "category":category,
            "list_price":float(list_price),
            "best_price":float(best_price),
            "card_price": 0,
            "web_dsct":float(dsct),
            "link": link,
            "image": image,
            "date":current_day,
            "market":market,
            "time":current_time
            }}
            collection2.update_one(filter,newvalues)
               
        else:
            print("ADICIONA NUEVO REGISTRO A BD ")
            
            
            data =  {
            "_id":market+str(sku),   
            "sku":str(sku), 
            "brand":brand,
            "product": product,
            "category":category,
            "list_price":float(list_price),
            "best_price":float(best_price),
            "card_price": 0,
            "web_dsct":float(dsct),
            "link": link,
            "image": image,
            "date":current_day,
            "market":market,
            "time":current_time
            }

            collection2.insert_one(data)
            
scrap(web)

# def scrap_category(category_url, category_on_bd):
#     for i in range(50):
#         success = scrap(category_url+str(i+1), category_on_bd)
#         if success == False:
#             return

# path = "C:\\Git\\fala\\wong\\text\\url.txt" #  WINDOWS
# #th = "wong//text//url.txt" # MAC OR LINUX


# web = open(path_wong,"r").readlines()
# links = []
# for url in web:
#     link = url.strip().split()
#     links.append(link)

# webs = []
# for i,v in enumerate(links):
#     for e in range (50):
#      a=links[i][0]+str(e+1)+links[i][1]
#      webs.append(a)

# def wong ():
#     for id, val  in enumerate (webs):
        
#         scrapping = scrap(val)
#         if scrapping == False:
#                 continue
    

#     auto_telegram()

# wong()