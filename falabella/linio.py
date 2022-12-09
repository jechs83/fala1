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
    


    # try:
    #  error = soup.find( "div", id= "NE-2-titulo-principal" ).text
    # except: error = None
    # print(type(error))

  
    # print()
    # if type(error) ==  str:
    #     return True

    try:
     data = soup.find("script", id="__NEXT_DATA__" ).text
    except: return False

    js = json.loads(data)
    try:
     x = js["props"]["pageProps"]["results"]

    except: return False

    for i in range (49):
       
        try:
         brand = x[i]["brand"]
        except: brand= "None"

        try:
         product = x[i]["displayName"]
        except: product= "None"

        try:
         web_dsct = x[i]["discountBadge"]["label"]
         web_dsct = web_dsct.replace("-","").replace("%","")
        except: web_dsct =0

        try:
         image = x[i]["mediaUrls"][0]
        except:  
            try:    
             image = x[i]["mediaUrls"]
            except: image = "None"

        try:
         sku = x[i]["skuId"]
        except: sku = 0

        if sku ==0:
            continue

        try:
         link = x[i]["url"]
        except: link = "None"

        try:
         card_price = x[i]["prices"][0]["price"][0]
         card_price = card_price.replace(",","")
        except: card_price = 0

        try:
         best_price = x[i]["prices"][1]["price"][0]
         best_price = best_price.replace(",","")
        except: best_price= 0

        try:
         list_price= x[i]["prices"][2]["price"][0]
         list_price = list_price.replace(",","")
        except: list_price = 0 

      
        # print()
        # print( "producto numero "+ str(i+1));
        # print(sku);print(brand);print(product);print("list price "+str(list_price));print("best price "+str(best_price));print("card price "+str(card_price));
        # print("descuento "+str(web_dsct)); print("link "+link)
        

        bd_name_store = "linio"
        collection = "market"  #   NOMBRE DE BASE DE DATOS
        market = "linio"    # COLECCION
        dsct = web_dsct
        card_dsct = 0
        date_time = load_datetime()

        save_data_to_mongo_db(bd_name_store,collection, market,sku,brand,product,list_price,
                            best_price,card_price,link,image,dsct, card_dsct, date_time[0] ,date_time[1])


# def scrap_category(category_url):
#     for i in range(500):

#         success = scrap(category_url+str(i+1))
#         print(category_url+str(i+1))
#         #time.sleep(3)
#         if success == False:
#             return


array_tec=[]

#arg_ = sys.argv[1]
num = sys.argv[1]
arg_ = config("SAGA_TEXT_PATH")+str(num)+".txt"

f = open(arg_, "r")
x = f.readlines()

for i in x:
    #print(i)
    array_tec.append(i.split()) 

count = len(array_tec)
print(count)
def saga_scrapper():
    
    for id, val in enumerate(array_tec):
    #print(val[0], val[1])
     url_count = id-1

     for i in range(500):
      
    
        success = scrap(val[0]+str(i+1)+val[1])
        print(val[0]+str(i+1)+val[1])
        #time.sleep(3)
        if success == False:
            break
 
        
        print(id, count-1)
        if id == count-1 :

            print("se acabo la web y va comenzar a dar vueltas")ß
            time.sleep(10)
            
            saga_scrapper() 
        



saga_scrapper()








    