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
        if i == 1:
            break
        print(i)
       

        
        # try:
        #  brand = i.find("div", class_="Showcase__brand").text
        # except: brand = None
        # print(brand)
        # link = i.find("a", class_="Showcase__link").attrs.get("href")
        # print(link)
        # try:
        #     list_price = i.find("div", class_="Showcase__oldPrice").text
        # except: list_price = 0
        # list_price = str(list_price).replace("S/","").replace(",","")
        # print(str(list_price).strip())


        # try:
        #     best_price = i.find("div", class_="Showcase__salePrice").text
        # except: best_price = 0
        # best_price = best_price.replace("S/","").replace(",","")
        # print(best_price.strip())
        
        
        # sku = i.find("li", class_="helperComplement").attrs.get("id")
        # print(sku)
        

    

        





        
    
scrap(web)
        
#         sku = i.find("div",class_="product-item").attrs.get("data-sku")
#         brand = i.find("div",class_="product-item").attrs.get("data-brand")
#         category = i.find("div",class_="product-item").attrs.get("data-category")
#         product = i.find("div",class_="product-item").attrs.get("data-name")
#         list_price = i.find("div",class_="product-item").attrs.get("data-price")
#         list_price = list_price.split()[1].replace(",","")
#         try:
#             best_price = i.find("span", class_="product-prices__value--best-price").text
#             best_price = best_price.split()[1].replace(",","")
#         except:best_price = 0
#         link = i.find("div",class_="product-item").attrs.get("data-uri")
#         img = i.find("img").attrs.get("src")
#         market= "wong"
#         try:
#             dsct = i.find("div", class_= "flag discount-percent").text
#             dsct= dsct.replace(",",".").replace("%","")
#         except: dsct = 0

#         print()
#         print(product)
#         print(url) 
#         print(best_price) 
#         print(sku) 
#         print(brand)
#         print(dsct)
#         print(category)
#         print(list_price) 
#         print(link) 
#         print(img)
#         print()

#         db = client["cencosud"]
#         collection = db["market"]
#         db2 = client["scrap"]
#         collection2 = db2["scrap"]
#         market = "wong"
        

#         y = collection.find_one({"_id":market+str(sku)})
#         z = collection2.find_one({"_id":market+str(sku)})

#         if y :
            
#             filter = {"_id":market+str(sku), }
#             newvalues = { "$set":{ 
#             "_id":market+str(sku),   
#             "sku":str(sku), 
#             "brand":brand,
#             "product": product,
#             "category":category,
#             "list_price":float(list_price),
#             "best_price":float(best_price),
#             "card_price": 0,
#             "web_dsct":float(dsct),
#             "link": link,
#             "image": img,
#             "image2": "=IMAGE("+'"'+img+'"'+")",
#             "date":current_day,
#             "market":market,
#             "time":current_time
#             }}
#             collection.update_one(filter,newvalues)
               
#         else:
#             print("ADICIONA NUEVO REGISTRO A BD ")
            
            
#             data =  {
#             "_id":market+str(sku),   
#             "sku":str(sku), 
#             "brand":brand,
#             "product": product,
#             "category":category,
#             "list_price":float(list_price),
#             "best_price":float(best_price),
#             "card_price": 0,
#             "web_dsct":float(dsct),
#             "link": link,
#             "image": img,
#             "image2": "=IMAGE("+'"'+img+'"'+")",
#             "date":current_day,
#             "market":market,
#             "time":current_time
            
#             }

#             collection.insert_one(data)
            
       
#         y = collection2.find_one({"_id":market+str(sku)})

#         if z :
            
#             filter = {"_id":market+str(sku), }
#             newvalues = { "$set":{ 
#             "_id":market+str(sku),   
#             "sku":str(sku), 
#             "brand":brand,
#             "product": product,
#             "category":category,
#             "list_price":float(list_price),
#             "best_price":float(best_price),
#             "card_price": 0,
#             "web_dsct":float(dsct),
#             "link": link,
#             "image": img,
#             "image2": "=IMAGE("+'"'+img+'"'+")",
#             "date":current_day,
#             "market":market,
#             "time":current_time
#             }}
#             collection2.update_one(filter,newvalues)
               
#         else:
#             print("ADICIONA NUEVO REGISTRO A BD ")
            
            
#             data =  {
#             "_id":market+str(sku),   
#             "sku":str(sku), 
#             "brand":brand,
#             "product": product,
#             "category":category,
#             "list_price":float(list_price),
#             "best_price":float(best_price),
#             "card_price": 0,
#             "web_dsct":float(dsct),
#             "link": link,
#             "image": img,
#             "image2": "=IMAGE("+'"'+img+'"'+")",
#              "date":current_day,
#             "market":market,
#             "time":current_time
#             }

#             collection2.insert_one(data)
            
        

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