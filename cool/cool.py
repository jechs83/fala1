import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import sys
import pytz
import random
import time
from decouple import config
from bd_record import save_data_to_mongo_db
from datetime import datetime
from datetime import date
import json


web_url = random.choice(config("PROXY"))
client = MongoClient(config("MONGO_DB"))

def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now




def shop(web):

    proxies = {"http":"http://"+web_url }
    res=requests.get(web,  proxies= proxies)
    print(res.status_code)
    soup = BeautifulSoup(res.text, "html.parser")

    soup = soup.find_all("script")
    count = 0

    for i in soup:
        count = count+1
        if count <=8:
        
        #data = json.loads(i)
            print("#######################################################")
            print(i)
           
            data = json.loads(i)
            with open ( "/Users/javier/GIT/fala/cool/source.txt", "w+") as t:
                t.write(str(data))
            
        if count ==9:
            break
        # count = count+1
        # if count >= 8:
        #     print(i.text["__STATE__"])
        #     print("####################################")
        #     
        #     time.sleep(5)
        #     break
   
        
    


    elements=soup.find_all("div", class_="coolboxpe-search-result-0-x-galleryItem coolboxpe-search-result-0-x-galleryItem--container-galleryProductos coolboxpe-search-result-0-x-galleryItem--normal coolboxpe-search-result-0-x-galleryItem--container-galleryProductos--normal coolboxpe-search-result-0-x-galleryItem--list coolboxpe-search-result-0-x-galleryItem--container-galleryProductos--list pa4")
    # if not elements:
    #     return False

   
    
    for idx, i in enumerate(elements):
    
        print(elements)
        try:
            brand=i.find( "span", class_="vtex-store-components-3-x-productBrandName").text
        except: brand = "Null"
        print(brand)

        try:
            product=i.find( "img" ).attrs.get("alt")
            product = product.strip()
        except: product = None

        try:
            sku=i.find("div", class_="product-item-inner").find("form").attrs.get("data-product-sku")
        except: sku = 0

        try:
            list_price=i.find("div", class_="price-box price-final_price").find("span",class_="old-price").find("span", class_="price").text
            list_price = list_price.replace("S/","").replace(",","").replace("S/. ","")
        except: list_price=0

        try:
            best_price=i.find("div", class_="price-box price-final_price").find("span",class_="price-container price-final_price tax weee").find("span", class_="price").text

            best_price = best_price.replace("S/","").replace(",","").replace("S/. ","")
        except: best_price=0

    
        try:
            link=i.find("a").attrs.get("href")
        except: link = None
      
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

        bd_name_store = "cool"
        collection = "cool"
        market = "cool"
        card_price = 0
        card_dsct =0
        dsct = web_dsct
        date_time = load_datetime()
        print(),print(brand),print(sku),print(product) ,print(link),print(category),print("LIST PRICE")
        print(list_price)
        print("best price")
        print(best_price)#print(image),print(market),print(web_dsct)

        save_data_to_mongo_db(bd_name_store,collection, market,str(sku),brand,product,list_price,
                            best_price,card_price,link,image,dsct, card_dsct, date_time[0] ,date_time[1])


array_tec=[]

num = sys.argv[1]
arg_ = config("COOLBOX_TEXT_PATH")+str(num)+".txt"

f = open(arg_, "r")
x = f.readlines()

for i in x:
    array_tec.append(i.rstrip())



count  = len(array_tec)
def promart_scrap():
    try:
        for i,v in enumerate(array_tec):
            print(array_tec)

            for e in range(1):
              
                x = shop(v+str(e+1))
                print(v+str(e+1))

                if x == False:
                    print("SE PARA PIRQUE NO  HAY MAS ")
                    print(x)
                    promart_scrap()

            # if i == count-1:
            #     print("se acabo la web y va comenzar a dar vueltas")
            #     time.sleep(5)
                
            #     promart_scrap()
    except:
        return promart_scrap()

        


promart_scrap()