
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
from multiprocessing import Pool, freeze_support

web_url = random.choice(lines)
client = MongoClient(config("MONGO_DB"))

def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now

# first_sku = None
HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

def scrap (web):
    # global first_sku
    proxies = {"http":"http://"+web_url }
        
    print(web)
    print("#####################################################################################")
    res=requests.get(web,  proxies= proxies, headers = HEADERS)
    print("Respuesta del servidor :"+str(res.status_code))
    response = res.status_code

    # if response != 200:
    #     pass

    soup = BeautifulSoup(res.text, "html.parser")
    try:
      no_page = soup.find("div",class_="error-page-container")
    except:
        no_page=None
    print(no_page)
    # if no_page == None:
    #     return False
    # print(no_page)


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
        

        # if  sku == first_sku:
        #     print("se repite SKU")
        #     return False 

        # if count == 1:
        #     first_sku = sku

        try:
            dsct= i.find(class_="catalog-product-details__discount-tag")
            dsct= dsct.text.replace("-","").replace("%","")
        except:
            dsct= 0
        # if dsct == 0:
        #     continue

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

        # print()
        # print(brand)
        # print(product)
        # print(link)


       
        bd_name_store = "ripley"
        collection = "market"  #   NOMBRE DE BASE DE DATOS
        market = "ripley"    # COLECCION
        card_dsct = 0
        date_time = load_datetime()
        
        save_data_to_mongo_db(bd_name_store,collection, market,sku,brand,product,list_price,
                             best_price,card_price,link,image,dsct, card_dsct, date_time[0] ,date_time[1],web)
     
       

   

num = sys.argv[1]

array_tec=[]
arg_ = sys.argv[1]
num = sys.argv[1]
arg_ = "/Users/javier/GIT/fala/ripley/urls/test/ripley"+str(num)+".txt"

f = open(arg_, "r")
x = f.readlines()
for i in x:
    #array_tec.append(i.rstrip()) 
    array_tec.append(i.split()) 
        


lista = []
inicio = None
for i,v  in enumerate  (array_tec):
    if i ==0:
        inicio = load_datetime()
    for i in range (int(v[1])):
        lista.append(v[0]+str(i+1))


    if __name__ == '__main__':

            freeze_support()
            p = Pool()
            p.map (scrap,lista)
            p.terminate()
            p.join()
    lista=[]
        

print(inicio)
print(load_datetime())


# inicio =None
# for i in range (15):
#     if i == 0:
#      inicio = load_datetime()
#     web = "https://simple.ripley.com.pe/tecnologia/celulares/celulares-y-smartphones?page="+(str(i+1))

#     scrap(web)


# print(inicio)
# print(load_datetime())






    