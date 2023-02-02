
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import sys
from datetime import datetime
import pytz
import random
import time
from bd_record import save_data_to_mongo_db
from decouple import config
text_file = open(config("PROXY"), "r")
lines = text_file.readlines() 
from datetime import datetime
from datetime import date

web_url = random.choice(lines)
client = MongoClient(config("MONGO_DB"))

def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now

first_sku = None

def scrap (web):
    global first_sku
    proxies = {"http":"http://"+web_url }
        
    print(web_url)
    print("#####################################################################################")
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

        image_start = image[:6]
        if image_start != "https:":
             image = "https:"+image
    

        sku = i.find(class_="catalog-product-item catalog-product-item__container undefined").attrs.get("id")
        sku = str(sku)   
        
        #print(str(sku)+" "+ str(first_sku))

        if  sku == first_sku:
            print("se repite SKU")
            #print(str(sku)+" "+ str(first_sku))
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


       
        bd_name_store = "ripley"
        collection = "market"  #   NOMBRE DE BASE DE DATOS
        market = "ripley"    # COLECCION
        card_dsct = 0
        date_time = load_datetime()
        
        save_data_to_mongo_db(bd_name_store, market,sku,brand,product,list_price,
                            best_price,card_price,link,image,dsct, card_dsct, date_time[0] ,date_time[1],web)
       

    time.sleep(2)      



num = sys.argv[1]
def urls_list( id):
    
    db = client["ripley"]
    collection = db["lista"]
    
    x = collection.find({"_id":int(id)})
    for i in x:
        list = i["url"]
    return list
array_tec = urls_list(num)
count = len(array_tec)

db = client["trigger"]
collection = db["ripley"]

def bd_change(num, bd_status):
    
    
    x = collection.find_one({"_id":int(num)})
    if x  :
            #print(" ACTUALIZA BASE DE DATOS ")
        filter = {"_id":int(num)}
        newvalues = { "$set":{ 
        "status":bd_status, 
        }}
        collection.update_one(filter,newvalues)      

def ripley_scrap():
   
    for id, val in enumerate(array_tec):
        try:
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
        except:
             ripley_scrap()
                


ripley_scrap()










    