
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import sys
from datetime import datetime
import pytz
import random
import time
from bd_record import save_data_to_mongo_db

server_date = datetime.now()
timezone = pytz.timezone("America/Bogota")
peru_date = server_date.astimezone(timezone)
current_date = peru_date.strftime("%d/%m/%Y" )
current_time =peru_date.strftime("%H:%M" )
from decouple import config
web_url = random.choice(config("PROXY"))
client = MongoClient(config("MONGO_DB"))

first_sku = None

def scrap (web):
    global first_sku
    proxies = {"http":"http://"+web_url }
        
    res=requests.get(web,  proxies= proxies)
    print("Respuesta del servidor :"+str(res.status_code))

    soup = BeautifulSoup(res.text, "html.parser")
    try:
      no_page = soup.find("div",class_="error-page-container")
    except:
        no_page=None
    print("dddddd")
    print(no_page)
    # if no_page == None:
    #     return False
    # print(no_page)

    if res.status_code == 404:
        return False
    count=0
    productos = soup.find_all( "div", class_="catalog-product-item catalog-product-item__container col-xs-6 col-sm-6 col-md-4 col-lg-4")
    for i in productos:
    
        
        count +=1
        
        try:
            brand = i.find(class_="brand-logo").text
        except:
            brand= "None"
    
        product = i.find(class_="catalog-product-details__name").text

        image = i.find("img").attrs.get("data-src")

        

        sku = i.find(class_="catalog-product-item catalog-product-item__container undefined").attrs.get("id")
        sku = str(sku)   
        
      
        print(str(sku)+" "+ str(first_sku))

        if  sku == first_sku:
            print("se repite SKU")
            print(str(sku)+" "+ str(first_sku))
      
            return False 

        if count == 1:
            first_sku = sku

            
        

        
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

        print()
        print(brand)
        print(product)
        print(link)


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
            "brand":str(brand),
            "product": str(product),
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
            "brand":str(brand),
            "product": str(product),
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
            "brand":str(brand),
            "product": str(product),
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
            "brand":str(brand),
            "product": str(product),
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
       
            
            
    time.sleep(2)      



array_tec=[]
arg_ = sys.argv[1]
num = sys.argv[1]
arg_ = config("RIPLEY_TEXT_PATH")+str(num)+".txt"

f = open(arg_, "r")
x = f.readlines()

for i in x:
    array_tec.append(i.rstrip()) 

count =(len(array_tec))




def ripley_scrap():
    for id, val in enumerate(array_tec):
       
        
        for i in range(200):
            print("web numero "+str(id+1)+ " de 500 aprox")
            success = scrap(val+str(i+1))
            print(val+str(i+1))
            #time.sleep(3)
            if success == False:
                break

        if id == count-1:

                print("se acabo la web y va comenzar a dar vueltas")
                time.sleep(5)
                ripley_scrap()
            
        

ripley_scrap()

  







    