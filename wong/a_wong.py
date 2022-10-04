import sys
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime
from a_telegram import auto_telegram
import os
import json
import random
from g_var import mongo_db, proxies, path_wong
date = datetime.today().strftime('%d/%m/%Y')
date_now = datetime.today().strftime('%d/%m/%Y')
web_url = random.choice(proxies)
client = MongoClient(mongo_db)
def scrap (web):

    proxies = {"http":"http://"+web_url }
        
    res=requests.get(web,  proxies= proxies)
    print("Respuesta del servidor :"+str(res.status_code))

   
    res=requests.get(web,  proxies= proxies)
    soup = BeautifulSoup(res.text, "html.parser")
    #print(soup.prettify())
    try:
     elements = soup.find_all("li",layout="19ccd66b-b568-43cb-a106-b52f9796f5cd")
    except:
        return False

    for i in elements:
        
        sku = i.find("div",class_="product-item").attrs.get("data-sku")
        brand = i.find("div",class_="product-item").attrs.get("data-brand")
        category = i.find("div",class_="product-item").attrs.get("data-category")
        product = i.find("div",class_="product-item").attrs.get("data-name")
        list_price = i.find("div",class_="product-item").attrs.get("data-price")
        list_price = list_price.split()[1].replace(",","")
        try:
            best_price = i.find("span", class_="product-prices__value--best-price").text
            best_price = best_price.split()[1].replace(",","")
        except:best_price = 0
        link = i.find("div",class_="product-item").attrs.get("data-uri")
        img = i.find("img").attrs.get("src")
        market= "wong"
        try:
            dsct = i.find("div", class_= "flag discount-percent").text
            dsct= dsct.replace(",",".").replace("%","")
        except: dsct = 0

        print()
        print(product)
        print(url) 
        print(best_price) 
        print(sku) 
        print(brand)
        print(dsct)
        print(category)
        print(list_price) 
        print(link) 
        print(img)
        print()

        db = client["cencosud"]
        collection = db["market"]
        db2 = client["scrap"]
        collection2 = db2["scrap"]

        

        y = collection.find_one({"_id":market+str(sku)})
        z = collection2.find_one({"_id":market+str(sku)})

        if y :
            
            filter = {"_id":market+str(sku), }
            newvalues = { "$set":{ 
            "_id""_id":market+str(sku),   
            "sku":int(sku), 
            "brand":brand,
            "product": product,
            "category":category,
            "list_price":float(list_price),
            "best_price":float(best_price),
            "card_price": 0,
            "web_dsct":float(dsct),
            "link": link,
            "image": img,
            "image2": "=IMAGE("+'"'+img+'"'+")",
            "date":date_now
            }}
            collection.update_one(filter,newvalues)
               
        else:
            print("ADICIONA NUEVO REGISTRO A BD ")
            
            
            data =  {
            "_id":market+str(sku),   
            "sku":int(sku), 
            "brand":brand,
            "product": product,
            "category":category,
            "list_price":float(list_price),
            "best_price":float(best_price),
            "card_price": 0,
            "web_dsct":float(dsct),
            "link": link,
            "image": img,
            "image2": "=IMAGE("+'"'+img+'"'+")",
            "date":date_now
            }

            collection.insert_one(data)
            
       
        y = collection.find_one({"_id":market+str(sku)})

        if z :
            
            filter = {"_id":market+str(sku), }
            newvalues = { "$set":{ 
            "_id""_id":market+str(sku),   
            "sku":int(sku), 
            "brand":brand,
            "product": product,
            "category":category,
            "list_price":float(list_price),
            "best_price":float(best_price),
            "card_price": 0,
            "web_dsct":float(dsct),
            "link": link,
            "image": img,
            "image2": "=IMAGE("+'"'+img+'"'+")",
            "date":date_now
            }}
            collection2.update_one(filter,newvalues)
               
        else:
            print("ADICIONA NUEVO REGISTRO A BD ")
            
            
            data =  {
            "_id":market+str(sku),   
            "sku":int(sku), 
            "brand":brand,
            "product": product,
            "category":category,
            "list_price":float(list_price),
            "best_price":float(best_price),
            "card_price": 0,
            "web_dsct":float(dsct),
            "link": link,
            "image": img,
            "image2": "=IMAGE("+'"'+img+'"'+")",
            "date":date_now
            }

            collection2.insert_one(data)
            
        

def scrap_category(category_url, category_on_bd):
    for i in range(50):
        success = scrap(category_url+str(i+1), category_on_bd)
        if success == False:
            return

path = "C:\\Git\\fala\\wong\\text\\url.txt" #  WINDOWS
#th = "wong//text//url.txt" # MAC OR LINUX


web = open(path_wong,"r").readlines()
links = []
for url in web:
    link = url.strip().split()
    links.append(link)

webs = []
for i,v in enumerate(links):
    for e in range (50):
     a=links[i][0]+str(e+1)+links[i][1]
     webs.append(a)

def wong ():
    for id, val  in enumerate (webs):
        
        scrapping = scrap(val)
        if scrapping == False:
                continue
    

    auto_telegram()

wong()