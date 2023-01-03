import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import sys
from datetime import datetime
import random
import time
import json
from bd_record import save_data_to_mongo_db
from datetime import datetime
from datetime import date
from decouple import config

def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now

web_url = random.choice(config("PROXY"))
client = MongoClient(config("MONGO_DB"))


def scrap (web):

    proxies = {"http":"http://"+web_url }
    res=requests.get(web,  proxies= proxies)
    print("Respuesta del servidor :"+str(res.status_code))
    soup = BeautifulSoup(res.text, "html.parser")
    
    error = soup.find( "h3" , class_="jsx-860724461")
    print()
    print(error)
    print()
    if error:
        return False
    try:
     data = soup.find("script", id="__NEXT_DATA__" ).text
    except: return False


    js = json.loads(data)
    try:
     x = js["props"]["pageProps"]["initialData"]["products"]
    except: return False



    for i in range (32):
       

        try:
         brand = x[i]["title"]
        except: brand= "None"



        print(brand)


        try:
         product = x[i]["title"]
        except: product= "None"

        try:
         web_dsct = x[i]["discountBadge"]["label"]
         web_dsct = web_dsct.replace("-","").replace("%","")
        except: web_dsct =0

        try:
         image = x[i]["image"]
        except:  
             image = "None"
        print(image)


        try:
         link = x[i]["url"]
        except: link = "None"
        print(link)


        try:
         card_price = x[i]["prices"][0]["price"][0]
         card_price = card_price.replace(",","")
        except: card_price = 0

        try:
         best_price = x[i]["formated_current_price"]
         best_price = best_price.replace(",","").replace("S/","")[:-3].replace(".","")
        except: best_price= 0
        print(best_price)
        try:
         list_price= x[i]["formated_last_variation_price"]
         list_price = list_price.replace(",","").replace("S/","")[:-3].replace(".","")
         
        except: list_price = 0 
        print(list_price)
        try:
         sku = x[i]["product_id"]
        except: sku = 0
        print(sku)
        if sku ==0:
            continue

        try:
            dsct = x[i]["percent"]
            if dsct[:1] == "-":
                dsct = str(dsct).replace("-","")
                dsct = round(float(dsct))
        except: 
            dsct = 0

        

        print(dsct)
      


        # print()
        # print( "producto numero "+ str(i+1));
        # print(sku);print(brand);print(product);print("list price "+str(list_price));print("best price "+str(best_price));print("card price "+str(card_price));
        # print("descuento "+str(web_dsct)); print("link "+link)
        

        bd_name_store = "knasta"
        collection = "market"  #   NOMBRE DE BASE DE DATOS
        market = "knasta"    # COLECCION
        
        card_dsct = 0
        date_time = load_datetime()
        brand = "knasta"

        save_data_to_mongo_db(bd_name_store,collection, market,sku,brand,product,list_price,
                            best_price,card_price,link,image,dsct, card_dsct, date_time[0] ,date_time[1])


def scrap_category(category_url):
    for i in range(100):

        success = scrap(category_url+str(i+1))
        print(category_url+str(i+1))
        #time.sleep(3)
        if success == False:
            break


array_tec=[]

#arg_ = sys.argv[1]
num = sys.argv[1]
arg_ = config("KNASTA_TEXT_PATH")+str(num)+".txt"

f = open(arg_, "r")
x = f.readlines()

for i in x:
    array_tec.append(i.rstrip()) 

count = len(array_tec)

def saga_scrapper():
    
    for id, val in enumerate(array_tec):
        print(val)
    
        web = val
        
        scrap_category(web) ## GENERA LA LISTA DE PAGINACIONES POR CATEGORIA
        print("esta web es la numero "+str(id+1)+" de aprox 500")


        if id == count-1:
            print("se acabo la web y va comenzar a dar vueltas")
            time.sleep(10)
            
            saga_scrapper() 
        



saga_scrapper()








    