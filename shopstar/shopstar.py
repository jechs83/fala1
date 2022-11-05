import sys
import time
from pymongo import MongoClient
from datetime import date
import sys
sys.path.append('/Users/javier/GIT/fala') 
import requests
from bs4 import BeautifulSoup
import re
import time
import random
current_time= time.strftime("%H:%M")
date = date.today()
current_day= date.strftime("%d/%m/%Y")

from decouple import config
web_url = random.choice(config("PROXY"))
client = MongoClient(config("MONGO_DB"))



def shop(web):

    #headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"}
    proxies = {"http":"http://183.111.25.248:8080" }

    res=requests.get(web,  proxies= proxies)
    print("Servidor reponde "+str((res.status_code)))
   
    soup = BeautifulSoup(res.text, "html.parser")
        
    elements=soup.find_all("div",class_="product")
   
    if not elements:
        return True
    
  
    for idx, i in enumerate(elements):

        try:
         sku= i.find("div", class_="buy-button-normal").attrs.get("id")
        except:
            sku = None
        

        #print(i.prettify())
        brand = i.find("h6", class_="x-brand").text
        product = i.find("h6", class_="x-name").text
        try:
         list_price= i.find(class_="product__old-price").text
         list_price = list_price.replace("S/. ","").replace(",","")
        except: list_price = 0
        try:
         best_price= i.find("span", class_="product__price").text
         best_price = best_price.replace("S/. ","").replace(",","")
        except: best_price = 0
       
        try:
            web_dsct= i.find(class_="product__discount").text
            web_dsct= web_dsct.replace("-","").replace(",",".").replace(" %","").replace(" ","")
        except: web_dsct = 0

        try:
            ibk_dsct = i.find(class_="contentFlag").text
            ibk_dsct = ibk_dsct.split()[1].replace("%","")
            card_dsct=float(web_dsct)+float(ibk_dsct)
            card_price = (float(best_price)*(100-float(ibk_dsct))/100)
        except: card_dsct = 0

        if card_dsct==0:
            card_price=0

        try:
          image = i.find("img").attrs.get("src")
        except: image = "Null"
        link = i.find("a").attrs.get("href")
        market= "shopstar"
        category = i.attrs.get("data-cate")
 
        market = "shopstar"
        db = client["shopstar"]
        collection = db["market"]
        db_max = client["scrap"]
        collection_max = db_max["scrap"]
        x = collection.find_one({"_id":market+sku})
        y = collection_max.find_one({"_id":market+sku})
        
        

        if x  :
                filter = {"_id":market+sku}
                newvalues = { "$set":{ 

                "brand":brand,
                "sku":sku,
                "market":market,
                "product": product,
                "list_price":float(list_price),
                "best_price":float(best_price),
                "card_price":float(card_price),
                "web_dsct":float(web_dsct),
                "card_dsct":float(card_dsct),
                "category":category,
                "link": str(link),
                "image":str(image),
                "date":current_day,
                "time":current_time
            
                }}
                collection.update_one(filter,newvalues)
         
        else:
                data =  {
                "_id":market+sku, 
                "brand":brand,
                "sku":sku,
                "market":market,
                "product": product,
                "list_price":float(list_price),
                "best_price":float(best_price),
                "card_price":float(card_price),
                "web_dsct":float(web_dsct),
                "card_dsct":float(card_dsct),
                "category":category,
                "link": str(link),
                "image":str(image),
                 "date":current_day,
                "time":current_time
                    }
                collection.insert_one(data)
           
                
        if y :
                filter = {"_id":market+sku}
                newvalues = { "$set":{ 

                "brand":brand,
                "sku":sku,
                "market":market,
                "product": product,
                "list_price":float(list_price),
                "best_price":float(best_price),
                "card_price":float(card_price),
                "web_dsct":float(web_dsct),
                "card_dsct":float(card_dsct),
                "category":category,
                "link": str(link),
                "image":str(image),
                "date":current_day,
                "time":current_time
            
                }}
               
                collection_max.update_one(filter,newvalues)
        else:
                data =  {
                "_id":market+sku, 
                "brand":brand,
                "sku":sku,
                "market":market,
                "product": product,
                "list_price":float(list_price),
                "best_price":float(best_price),
                "card_price":float(card_price),
                "web_dsct":float(web_dsct),
                "card_dsct":float(card_dsct),
                "category":category,
                "link": str(link),
                "image":str(image),
                 "date":current_day,
                "time":current_time
                    }
               
                collection_max.insert_one(data)
                
        # print("product number "+ str(idx+1));print(brand);print(product);print(sku);print(category);print(list_price);print(best_price);print(card_price);
        # print(web_dsct);print(card_dsct);print(link);print("##################");print()


def scrapero(web):

    for i in range(1000):
        x = shop(web+str(i+1))
        print(web+str(i+1))
        if x == True:
            print(x)
            return False

        print("pagina "+str(i+1))

  
array_tec=[]
# lista de proxies
arg_ = sys.argv[1]
f = open(arg_, "r")
x = f.readlines()
for i in x:
    array_tec.append(i.rstrip())

array_tec=[]
# lista de proxies
arg_ = sys.argv[1]
f = open(arg_, "r")
x = f.readlines()
for i in x:
    array_tec.append(i.rstrip())


for i,v in enumerate(array_tec):
    scrap =  scrapero(v)
    if scrap == False:
       continue
 

# falta esta url
#https://shopstar.pe/electrohogar/cuidado-personal
#https://shopstar.pe/belleza-y-cuidado-personal/cuidado-del-bebe