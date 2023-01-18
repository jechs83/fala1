import sys
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime
import os
import json
import random
from datetime import date
import json
import time
from bd_record import save_data_to_mongo_db
from datetime import datetime
from datetime import date
from decouple import config

web_ram = random.choice(config("PROXY"))
client = MongoClient(config("MONGO_DB"))

def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now

web ="https://www.oechsle.pe/tecnologia?&optionOrderBy=OrderByScoreDESC&optionOrderBy=OrderByScoreDESC&O=OrderByScoreDESC&optionOrderBy=OrderByScoreDESC&page=1"
def scrap (web):

    proxies = {"http":"http://"+web_ram }

    res=requests.get(web,  proxies= proxies)
    print("Respuesta del servidor :"+str(res.status_code))
    soup = BeautifulSoup(res.text, "html.parser")

    soup = soup.find_all("script")

    array = []
    count = 0
    for i in soup:

    
        count = count+1
        if count == 30:
            text = i.text
            text= text.replace("vtex.events.addData(","")
            text = text[:-3]
            #print(text)

            data = json.loads(text)
            #print(data)

            productos = data["shelfProductIds"]
            for i in productos:
                array.append("productId:"+i)

       
        web1= "https://www.oechsle.pe/api/catalog_system/pub/products/search/?fq="
        web2=  ",".join(array)
        web3 = "&_from=0&_to=49"

        url = web1+web2+web3





    res = requests.get(url, proxies = proxies).json()
    #print("Respuesta del servidor :"+str(res.status_code))

    print(url)
    for idx,i   in  enumerate (res):
        try:
            sku = i["SKU"][0]
        except:
            return False
  
        product = i["productName"]
        brand = i["brand"]
        link= i["link"]
        image = i["items"][0]["images"][0]["imageUrl"]
        list_price = i["items"][0]["sellers"][0]["commertialOffer"]["Installments"][0]["Value"]
        # best_price=   i["items"][0]["sellers"][0]["commertialOffer"]["Price"]
        # stock=  i["items"][0]["sellers"][0]["commertialOffer"]["IsAvailable"]
        # try:
       
        #  dsct = (list_price*100/best_price)-100
        # except: dsct = 0
       
        # if dsct == 100:
        #     dsct = 0
        # dsct = round(dsct)
        print()
        print(brand)
        print(product)
        print(sku)
        print(link)
        print(image)
        print(list_price)
        # print(dsct)
        # print(best_price)
        # print(stock)

        bd_name_store = "oh"
        collection = "market"  #   NOMBRE DE BASE DE DATOS
        market = "oh"    # COLECCION
        card_price = 0 
        card_dsct = 0
    
  
        
        date_time = load_datetime()
        # save_data_to_mongo_db(bd_name_store,collection, market,sku,brand,product,list_price,
        #                     best_price,card_price,link,image,dsct, card_dsct, date_time[0] ,date_time[1])

 
       



array_tec=[]

num = sys.argv[1]

arg_ = config("OH_TEXT_PATH")+str(num)+".txt"

f = open(arg_, "r")


for i in f:
    array_tec.append(i.rstrip()) 
count = len(array_tec)



def vea_scrapper():
    try:
        for id, web in enumerate(array_tec):

        
            for i in range (200):
      
                success = scrap(web+(i+1))
                print(web+i+1)

                time.sleep(1000)
                if success == False:
                    break
    except:
        vea_scrapper()
    


scrap(web)
 ## GENERA LA LISTA DE PAGINACIONES POR CATEGORIA
        #print("esta web es la numero "+str(id+1)+" de aprox 500")

        # if success == False:
        #     continue
        # if id == count-1:
        #     print("se acabo la web y va comenzar a dar vueltas")
        #     time.sleep(10)
            
        #     vea_scrapper() 
#   except:
#     vea_scrapper()
        










    