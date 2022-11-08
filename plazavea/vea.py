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

#web = "https://www.plazavea.com.pe/tecnologia/televisores?page=2"
def scrap (web):

    proxies = {"http":"http://"+web_url }
        
    res=requests.get(web,  proxies= proxies)
    print("Respuesta del servidor :"+str(res.status_code))

   
    res=requests.get(web,  proxies= proxies)
    soup = BeautifulSoup(res.text, "html.parser")

    soup = str(soup)
    with open ("/Users/javier/GIT/fala/plazavea/json.txt", "w") as f:
      f.write(soup)
      x = f.read()
    json_data = json.load(x)


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
        list_price = str(list_price).strip()
        print(list_price)


        try:
            best_price = i.find("div", class_="Showcase__salePrice").text
        except: best_price = 0
        best_price = best_price.replace("S/","").replace(",","")
        best_price = best_price.strip()
        print(best_price)

        
        try:
            image = i.find("figure", class_="Showcase__photo").find("img").attrs.get("src")
        except: image = None
        print(image)

        sku = i.find("div", class_="g-producto")
        print(sku)
        try:
         dsct = (float(best_price)*100/float(list_price) )
        except: dsct = 0
        print(round(dsct,2))

        db = client["plazavea"]
        collection = db["market"]
        db2 = client["scrap1"]
        collection2 = db2["scrap1"]
        market = "vea"
    
        category = None
        dsct =None
        dsct= 0

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
            

web = open(config("VEA_TEXT_PATH"),"r").readlines()
links = []
for url in web:
  
    links.append(url.rstrip())



webs = []
for i,v in enumerate(links):
    for e in range (200):

        a=v+str(e+1)
 
        webs.append(a)



# def vea_scrapping ():

#     for id, val  in enumerate (webs):

#         scrapping = scrap(val)
#         print(scrapping)
#         print(val)
#         if scrapping == False:
#             continue
        
     
                
            
# vea_scrapping() 

scrap("https://www.plazavea.com.pe/api/catalog_system/pub/products/search?fq=C:/678/683/&_from=1&_to=20&O=OrderByScoreDESC&")