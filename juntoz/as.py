
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

first_sku = None
def scrap (web):
    global first_sku
    proxies = {"http":"http://"+web_url }
        
    print(web)
    print("#####################################################################################")
    res=requests.get(web,  proxies= proxies)
    print("Respuesta del servidor :"+str(res.status_code))

    soup = BeautifulSoup(res.text, "html.parser")


    print(web)

    productos = soup.find_all( "div", id="product-preview-card")

    if not productos:
        return False
    for i in productos:
        
        product = i.attrs.get("title")
        sku = i.find("input", class_="skuProductCatalog" ).attrs.get("value")

        if not sku:
            return False
        brand = i.find("a" ,class_="product-preview-card__wrapper__heading__product-brand").attrs.get("title")
        try: 
         dsct = i.find("div", class_="product-preview-card__wrapper__heading__product-discount").text
        except:
            dsct = 0
        web_dsct = str(dsct).strip().replace("%","")
        web_dsct  = web_dsct.rstrip()
        link = i.find("a", class_="product-preview-card__wrapper__body__main-image" ).attrs.get("href")
        link= "https://juntoz.com/"+link
        image = i.find("img").attrs.get("src")
        try:
         list_price = i.find("span", class_="product-preview-card__wrapper__footer__product-price__current-price").attrs.get("jztm-content")
        except:
            list_price = 0
        try:
         best_price = i.find("span", class_="product-preview-card__wrapper__footer__product-price__old-price" ).attrs.get("jztm-content")
        except:
            best_price = 0
        print()
        print(brand)
        print(product)
        print(sku)
        print(list_price)
        print(best_price)
        print(web_dsct)
        print(link)
        print(image)
        # count +=1
        url = web

        bd_name_store = "juntoz"
        collection = "market2"  #   NOMBRE DE BASE DE DATOS
        market = "juntoz"    # COLECCION
        card_dsct = 0
        card_price = 0
        date_time = load_datetime()
        
        save_data_to_mongo_db(bd_name_store, collection, market,sku,brand,product,list_price,
                            best_price,card_price,link,image,web_dsct, card_dsct, date_time[0] ,date_time[1], url)

        
   

num = sys.argv[1]
#arg_ = "C:\\GIT\\fala\\shopstar\\urls\\shop"+str(num)+".txt"
arg_ = "/Users/javier/GIT/fala/juntoz/urls/test/juntoz"+str(num)+".txt"


array_tec=[]

f = open(arg_, "r")
x = f.readlines()
for i in x:
    array_tec.append(i.split()) 



lista = []

for idx, val in enumerate  (array_tec):
  
    for i in range (500):
        lista.append(val[0]+str(i*28)+"&orderBy=rating-desc")
        


    if __name__ == '__main__':

        freeze_support()
        p = Pool(10)
        p.map (scrap,lista )
        p.terminate()
        p.join()
    


    
        lista=[]











    