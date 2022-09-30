import sys
sys.path.append('/Users/javier/GIT/fala') 
import sys
import time
from pymongo import MongoClient
import requests
import re
from datetime import date
from bs4 import BeautifulSoup
from webs_category import array_tec
from wong.g_var import mongo_db
date = date.today()

current_time= time.strftime("%H:%M")
current_date= date.strftime("%d/%m/%Y")


client = MongoClient(mongo_db)

db = client["shopstar"]
collection = db["promart"]

first_sku=""

def shop(web):
    global first_sku
    #headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"}
    proxies = {"http":"http:218.75.38.154:9091" }

    res=requests.get(web,  proxies= proxies)
    print("Servidor responde: "+ str(res.status_code))
   
    soup = BeautifulSoup(res.text, "html.parser")

    # file = open("/Users/javier/GIT/fala/promart/source.txt", "w+")
    # file.write(soup.prettify())
    # file.close
    
    elements=soup.find_all("div", class_="item-product product-listado")

    if not elements:
        return True
    
    
    
    for idx, i in enumerate(elements):
     
        try:
            link=i.find("a", class_="prod-det-enlace").attrs.get("href")
           
        except: link = None

        try:
            brand=i.find("div" ,class_="brand js-brand").text
        except: brand = "Null"

        try:
            best_price=i.find("div").attrs.get("data-best-price")
            best_price = best_price.replace("S/ ","").replace(",","").replace("S/. ","")
        except:
            best_price=0
            
        try:
            list_price=i.find("div").attrs.get("data-list-price")
            list_price = list_price.replace("S/ ","").replace(",","").replace("S/. ","")

            
        except: list_price = 0

        try:
            sku=i.find("div").attrs.get("data-id")
        
        except: sku = 0

     

        try:
            category=i.find("div").attrs.get("data-category")
           
        except: category = None


        try:
            product=i.find( "input" ,class_="insert-sku-quantity").attrs.get("title")
            
        except: product = None

        try:
            image=i.find( "img").attrs.get("src")
            
        except: image = None
        try:
         if best_price ==0 and list_price==0 or best_price == list_price:
            web_dsct=0
         else:
            web_dsct= float(list_price)-float(best_price)
            web_dsct = float(web_dsct)*100/float(list_price)
            web_dsct=round(web_dsct,2)
        except:web_dsct = 0

        market = "promart"
        # print()
        # print(brand)
        #print(sku)
        # print(product) 
        # print(link)
        # print(category)
        # print(list_price)
        # print(best_price)
        # print(image)
        # print(market)
        #print(web_dsct)

  
    
        x = collection.find_one({"_id":market+sku})

        if x:
                filter = {"_id":market+sku}
                newvalues = { "$set":{ 

                "_id":market+sku, 
                "brand":brand,
                "sku":sku,
                "market":market,
                "product": product,
                "list_price":float(list_price),           
                "best_price":float(best_price),
                "web_dsct":web_dsct,
                "category":category,
                "link": str(link),
                "image":str(image),
                "date":current_date,
                "time":current_time,
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
                 "web_dsct":web_dsct,
                "category":category,
                "link": str(link),
                "image":str(image),
                "date":current_date,
                "time":current_time,
                    }
                collection.insert_one(data)


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
 
