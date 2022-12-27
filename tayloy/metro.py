
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
from datetime import datetime
from datetime import date

proxy_list = random.choice(config("PROXY"))
client = MongoClient(config("MONGO_DB"))

urls = []

lista = open(proxy_list,"r")
for i in lista:
    urls.append(i)

web_url = random.choice(urls)

def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now


def scrap (web):
    print(web)
    proxies = {"http":"http://"+web_url }
    print(proxies)
    res=requests.get(web,  proxies= proxies)
    print(web)
    print("Respuesta del servidor :"+str(res.status_code))
    soup = BeautifulSoup(res.text, "html.parser")
    print(soup)
  
    count=0
    
    productos = soup.find_all( "li", layout="19ccd66b-b568-43cb-a106-b52f9796f5cd")

    if not productos:
        return False

    for i in productos:

        # print()
        # print("#########################################################")
        # print(i)
        
        count +=1
       
        print()
        link = i.find("a", class_="product-item__image-link").attrs.get("href")
        print(link)

        image = i.find("img").attrs.get("src")
        print(image)



        try:
            brand = i.find("div", class_="product-item__brand").text
            brand = brand.strip()
        except:
            brand = None
        print(brand)
      
        try:
         product = i.find("a" ,class_="product-item__name" ).attrs.get("title")
        except: product = None
        if product == None:
            return False
        print(product)

        try:
            best_price = i.find("span", class_="product-prices__value product-prices__value--best-price").text
            best_price = best_price.split()
            best_price= best_price[1].replace(",","")
        except: best_price = 0
        
        try:
            list_price = i.find("div", class_="product-prices__price product-prices__price--former-price").find("span", class_="product-prices__value").text
            list_price = list_price.split()[1].replace(",","")
        except: list_price = None

       
        if list_price == None:
            try:
                list_price = i.find("div", class_="price-box price-final_price").find("span", class_="price").text
                list_price = list_price.split()[1].replace(",","")
            except: list_price = 0
        print(best_price)
        print(list_price)

        try:
            produtc_id = i.find("button", class_="product-item__add-to-cart product-add-to-cart btn red add-to-cart").attrs.get("data-productid")
        except:
            continue

        sku = i.find("div", class_="product-item product-item--"+produtc_id).attrs.get("data-sku")
        sku = str(sku)   
        print(sku)
        try:
         dsct = 100-(float(best_price)*100/float(list_price))
         dsct = round(dsct)
        except: dsct = 0 
        print(round(dsct))

    
           
        # except: dsct = 0

        card_price = 0

        # print()
        # print(product)
        # print(brand)
        # print(image)
        # print(link)
        # print()
        # print("best price :" +str(best_price))
        # print("list price :"+str(list_price))
        # print(dsct)
        # # print(sku)
    
        bd_name_store = "metro"
        # collection = "market"  #   NOMBRE DE BASE DE DATOS
        market = "metro"    # COLECCION
        card_dsct = 0
        date_time = load_datetime()
        
        save_data_to_mongo_db(bd_name_store, market,sku,brand,product,list_price,
                            best_price,card_price,link,image,dsct, card_dsct, date_time[0] ,date_time[1])
       


web = "https://www.metro.pe/buscapagina?sl=19ccd66b-b568-43cb-a106-b52f9796f5cd&PS=18&cc=18&sm=0&PageNumber=1&&fq=C%3a%2f1001467%2f"

scrap(web)
'''


array_tec=[]
arg_ = sys.argv[1]
num = sys.argv[1]
arg_ = config("METRO_TEXT_PATH")+str(num)+".txt"

f = open(arg_, "r")
x = f.readlines()

for i in x:
    array_tec.append(i.split()) 

count =(len(array_tec))



# print(array_tec)

def metro_scrap():

    for id, val in enumerate(array_tec):
        
        for i in range(200):
            print("web numero "+str(id+1)+ " de 500 aprox")
            url = val[0]+str(i+1)+val[1]
            print(url)

            success = scrap(url)
                            
            print(url)
            #time.sleep(3)

            if success == False:
                print(success)
                break

        # if id == count-1:
        #         print("se acabo la web y va comenzar a dar vueltas")
        #         time.sleep(5)
        #         metro_scrap()




metro_scrap()
  
'''






    