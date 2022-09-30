import sys
import time
from pymongo import MongoClient
import sys 
import requests
from bs4 import BeautifulSoup
from wong.g_var import mongo_db, array_tec 
from proxy_list import proxies
import random
from datetime import datetime
import pytz
server_date = datetime.now()
timezone = pytz.timezone("America/Bogota")
peru_date = server_date.astimezone(timezone)
current_day = peru_date.strftime("%d/%m/%Y" )
current_time =peru_date.strftime("%H:%M" )
client = MongoClient(mongo_db)
web_url = random.choice(proxies)

ar_name= [], ar_product=[] , ar_product=[]

def shop(web):

    proxies = {"http":"http://"+web_url }

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
        x = collection.find_one({"_id":market+sku})

        if x:
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
     

for i,v in enumerate(array_tec):
    scrap =  scrapero(v)
    if scrap == False:
       continue
 

# falta esta url
#https://shopstar.pe/electrohogar/cuidado-personal
#https://shopstar.pe/belleza-y-cuidado-personal/cuidado-del-bebe