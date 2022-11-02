
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import sys
from datetime import datetime
import pytz
import random
import time
from g_var import mongo_db, proxies
server_date = datetime.now()
timezone = pytz.timezone("America/Bogota")
peru_date = server_date.astimezone(timezone)
current_date = peru_date.strftime("%d/%m/%Y" )
current_time =peru_date.strftime("%H:%M" )
client = MongoClient(mongo_db)
web_url = random.choice(proxies)
client = MongoClient(mongo_db)


def scrap (web):
  
    proxies = {"http":"http://"+web_url }
        
    res=requests.get(web,  proxies= proxies)
    print("Respuesta del servidor :"+str(res.status_code))

    soup = BeautifulSoup(res.text, "html.parser")
    try:
      no_page = soup.find("div",class_="error-page-container")
    except:
        no_page=None
    print(no_page)
    if no_page != None:
        return False
        
    count=0
    productos = soup.find_all( "div", class_="catalog-product-item catalog-product-item__container col-xs-6 col-sm-6 col-md-4 col-lg-4")
    for i in productos:
    
        count +=1

        try:
            brand = i.find(class_="brand-logo")
        except:
            brand= "None"
    
        product = i.find(class_="catalog-product-details__name")

        image = i.find("img").attrs.get("data-src")

        

        sku = i.find(class_="catalog-product-item catalog-product-item__container undefined").attrs.get("id")
        sku = str(sku)        
        
        try:
            dsct= i.find(class_="catalog-product-details__discount-tag")
            dsct= dsct.text.replace("-","").replace("%","")
        except:
            dsct= 0

        try:
            list_price= i.find(class_="catalog-prices__list-price catalog-prices__lowest catalog-prices__line_thru")
            list_price= list_price.text.replace("S/","").replace(",","")
        except:
            list_price= 0

        try:
            best_price = i.find(class_="catalog-prices__offer-price")
            best_price=best_price.text.replace("S/","").replace(",","")

        except:
            best_price = 0

        try:
            card_price = i.find(class_= "catalog-prices__card-price")
            card_price= card_price.text.replace("S/","").replace(",","")
        except:
            card_price= 0
        
        link = i.find(class_="catalog-product-item catalog-product-item__container undefined").attrs.get("href")
        link= "https://simple.ripley.com.pe"+link


        market = "ripley"
        db = client["ripley"]
        collection = db["market"]
        db_max = client["scrap"]
        collection_max = db_max["scrap"]

        x = collection.find_one({"_id":market+sku})
        y = collection_max.find_one({"_id":market+sku})
        
   
        if x  :
            #print(" ACTUALIZA BASE DE DATOS ")
            filter = {"_id":market+sku}
            newvalues = { "$set":{ 
            "_id":market+sku,   
            "sku":sku, 
            "market":market,
            "brand":str(brand.text),
            "product": str(product.text),
            "list_price":float(list_price),
            "best_price":float(best_price),
            "card_price": float(card_price),
            "link": str(link),
            "image": str(image),
            "date":current_date,
            "time":current_time
            }}
            collection.update_one(filter,newvalues)
 
            
        else:
            
            data =  {
            "_id":market+sku,     
            "sku":sku, 
            "market":market,
            "brand":str(brand.text),
            "product": str(product.text),
            "list_price":float(list_price),
            "best_price":float(best_price),
            "card_price": float(card_price),
            "web_dsct":float(dsct),
            "link": str(link),
            "image": str(image),
            "date":current_date,
            "time":current_time
            }
            collection.insert_one(data)
          
            
            
        if y :
            #print(" ACTUALIZA BASE DE DATOS ")
            filter = {"_id":market+sku}
            newvalues = { "$set":{ 
            "_id":market+sku,   
            "sku":sku, 
            "market":market,
            "brand":str(brand.text),
            "product": str(product.text),
            "list_price":float(list_price),
            "best_price":float(best_price),
            "card_price": float(card_price),
            "link": str(link),
            "image": str(image),
            "date":current_date,
            "time":current_time
            }}
           
            collection_max.update_one(filter,newvalues)
            
        else:
            
            data =  {
            "_id":market+sku,     
            "sku":sku, 
            "market":market,
            "brand":str(brand.text),
            "product": str(product.text),
            "list_price":float(list_price),
            "best_price":float(best_price),
            "card_price": float(card_price),
            "web_dsct":float(dsct),
            "link": str(link),
            "image": str(image),
            "date":current_date,
            "time":current_time
            }
          
            collection_max.insert_one(data)
       
            
            
    time.sleep(5)      
    return True



array_tec=[]

arg_=sys.argv[1]

f = open(arg_, "r")
x = f.readlines()
for i in x:
   array_tec.append(i.rstrip()) 
f.close

def scrap_category(category_url):
    for i in range(70):
        success = scrap(category_url+str(i+1))
        print(category_url+str(i+1))
        #time.sleep(3)
        if success == False:
            return

###########################################################
array_tec=[]
arg_ = sys.argv[1]

f = open(arg_, "r")
x = f.readlines()

for i in x:
    array_tec.append(i.rstrip()) 
webs= []
for i,v in enumerate(array_tec):
    for i in range (3):
        webs.append(v+(str(i+1)))

for id, val in enumerate(array_tec):
  
  web = val

  scrap_category(web) ## GENERA LA LISTA DE PAGINACIONES POR CATEGORIA
  
  

  







    