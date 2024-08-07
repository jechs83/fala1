
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
HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

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
        
    res=requests.get(web,  proxies= proxies, headers=HEADERS)
    print("Respuesta del servidor :"+str(res.status_code))

    soup = BeautifulSoup(res.text, "html.parser")
  
    count=0
    
    productos = soup.find_all( "li", class_="item product product-item")


    if not productos:
        return False

    for i in productos:

        
        count +=1

        link = i.find("a").attrs.get("href")
     
        try:
            brand = i.find("div", class_="brand-label").text
            brand = brand.strip()
     
        except:
            brand = None
      
        try:
         product = i.find("a", class_="product-item-link").text
         product = product.strip()
        except: product = None
        if product == None:
            return False

   

        image = i.find("img").attrs.get("src")

        try:
            best_price = i.find("span",class_="special-price").find("span", class_="price").text
            best_price = best_price.replace("S/","")
            best_price= best_price.replace(",","")
        except: best_price = 0

   
        
        try:
            list_price = i.find("span", class_="old-price").find("span", class_="price").text
            list_price = list_price .replace("S/","")
            list_price = list_price .replace(",","")
            
        except: list_price = None

        if list_price == None:
            try:
                list_price = i.find("span",class_="price-container price-final_price tax weee").find("span", class_="price").text
                list_price = list_price .replace("S/","")
                list_price = list_price .replace(",","")
            except: list_price = 0

        sku = i.find("div",class_="price-box price-final_price").attrs.get("data-product-id")
        sku = str(sku)   

        try:                
            # calculo = float(best_price)*100/float(list_price)
            # if calculo == 0:
            #     calculo =100
            # dsct = 100-calculo
            # dsct = round(dsct)
            dsct = i.find("div", class_="discount-box").find("span", class_="discount-value").text
            dsct = dsct.replace("-","").replace("%","")
            dsct  = dsct.strip()
        
        except: dsct = 0
        print(list_price)

        print(dsct)

        card_price = 0

        print()
        print(product)
        print(brand)
        print(image)
        print(link)
        print()
        print("best price :" +str(best_price))
        print("list price :"+str(list_price))
        print(dsct)
        print(sku)
        url = web
        card_dsct = 0
        print(url)
        bd_name_store = "tailoy"
        # collection = "market"  #   NOMBRE DE BASE DE DATOS
        bd_name_store = "tailoy"
        collection = "market"  #   NOMBRE DE BASE DE DATOS
        market = "tailoy"    # COLECCION\
        date_time = load_datetime()


        save_data_to_mongo_db(bd_name_store,collection, market,sku,brand,product,list_price,
                            best_price,card_price,link,image,dsct, card_dsct, date_time[0] ,date_time[1],web)
       

     




num = sys.argv[1]

def urls_list(id):
    
    db = client["tailoy"]
    collection = db["lista"]
    
    x = collection.find({"_id":int(id)})
    for i in x:
        list = i["url"]
    return list

array_tec = urls_list(num)
count = len(array_tec)
print(count)
print(array_tec)




def ripley_scrap():

    # try:
        for id, val in enumerate(array_tec):
        
            for i in range(200):
                print("web numero "+str(id+1)+ " de 500 aprox")
                print(val+str(i+1))
                success = scrap(val+str(i+1))
                print(val+str(i+1))
                #time.sleep(3)
                if success == False:
                    print(success)
                    break

            if id == count-1:
                    print("se acabo la web y va comenzar a dar vueltas")
                 
                    ripley_scrap()
    # except: 
    #     ripley_scrap()


ripley_scrap()




    