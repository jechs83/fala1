import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import sys
from datetime import datetime
import pytz
import random
import time
import json
from bd_record import save_data_to_mongo_db

server_date = datetime.now()
timezone = pytz.timezone("America/Bogota")
peru_date = server_date.astimezone(timezone)
current_date = peru_date.strftime("%d/%m/%Y" )
current_time =peru_date.strftime("%H:%M" )

from decouple import config
web_url = random.choice(config("PROXY"))

client = MongoClient(config("MONGO_DB"))
products_array = []

def scrap (web):

    global products_array
    proxies = {"http":"http://"+web_url }
    res=requests.get(web,  proxies= proxies)
    print("Respuesta del servidor :"+str(res.status_code))
    soup = BeautifulSoup(res.text, "html.parser")
    
    error = soup.find( "h3" , class_="jsx-860724461")
   
    if error:
        print();print(error);print()
        return False
    
    try:
        data = soup.find("script", id="__NEXT_DATA__" ).text
    except: data = None
    if data == None:
        return False

    js = json.loads(data)
    try:
     x = js["props"]["pageProps"]["searchProps"]["searchData"]["results"]

     #{"props":{"pageProps":{"searchProps":{"searchData":{"results":
    except: return False
    count = 0
    for i in range (55):
        count = count+1
        if count == 2:
            break
        try:
         brand = x[i]["brand"]
        except: brand= "None"
        print(brand)

        try:
         product = x[i]["displayName"]
        except: product= "None"

        # try:
        #  web_dsct = x[i]["discountBadge"]["label"]
        #  web_dsct = web_dsct.replace("-","").replace("%","")
        #  dsct = web_dsct
        # except: dsct =0

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

        # try:
        #  link = x[i]["url"]
        # except: link = "None"
        # try:
        #  card_price = x[i]["prices"][0]["price"][0]
        #  card_price = card_price.replace(",","")
        # except: card_price = 0

        # try:
        #  best_price = x[i]["prices"][1]["price"][0]
        #  best_price = best_price.replace(",","")
        # except: best_price= 0

        # try:
        #  list_price= x[i]["prices"][1]["price"][4]
        #  list_price = list_price.replace(",","")
        # except: list_price = 0 

        # try:   
        #  seller = x[i]["sellerName"]
        # except: seller = "None"
        
        print(product) 
        print(brand)
        print(sku)
        # market = "sodimac"
        # bd_name_store = "sodimac"
        # card_dsct = 0
        # page_array = [bd_name_store, market,sku,brand,product,list_price,
        #                     best_price,card_price,link,image,dsct, card_dsct]
        # products_array.append(page_array)


        
     
      

def scrap_category(category_url):
    for i in range(500):

        success = scrap(category_url+str(i+1))
        print(category_url+str(i+1))
        #time.sleep(3)
        if success == False:
            # print((products_array))

            # for idx, v in enumerate(products_array) :
               
                    
            #     save_data_to_mongo_db(v[0], v[1],v[2],v[3],v[4],v[5],
            #                 v[6],v[7],v[8],v[9],v[10], v[11])
               
   
            print("se termino de grabar")
            time.sleep(10)
            return


array_tec=[]

#arg_ = sys.argv[1]
num = sys.argv[1]
arg_ = config("SODIMAC_TEXT_PATH")+str(num)+".txt"

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








    