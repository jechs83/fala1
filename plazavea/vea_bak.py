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

def scrap (web):

    proxies = {"http":"http://"+web_ram }
    res = requests.get(web, proxies = proxies).json()
    #print("Respuesta del servidor :"+str(res.status_code))

    for idx,i   in  enumerate (res):

        sku = i["productReference"]
        product = i["productName"]
        brand = i["brand"]
        link= i["link"]
        image = i["items"][0]["images"][0]["imageUrl"]
        list_price = i["items"][0]["sellers"][0]["commertialOffer"]["ListPrice"]
        best_price=   i["items"][0]["sellers"][0]["commertialOffer"]["Price"]
        stock=  i["items"][0]["sellers"][0]["commertialOffer"]["IsAvailable"]
        dsct = (list_price*100/best_price)-100
        if dsct == 100:
            dsct = 0
        dsct = round(dsct)
        # print()
        # print(brand)
        # print(product)
        # print(sku)
        # print(link)
        # print(image)
        # print(list_price)
        # print(dsct)
        # print(best_price)
        # print(stock)

        bd_name_store = "plaza"
        collection = "market"  #   NOMBRE DE BASE DE DATOS
        market = "vea"    # COLECCION
        card_price = 0 
        card_dsct = 0
    
  
        
        date_time = load_datetime()
        save_data_to_mongo_db(bd_name_store,collection, market,sku,brand,product,list_price,
                            best_price,card_price,link,image,dsct, card_dsct, date_time[0] ,date_time[1])

    return True
       



        


# for i  in range (500):
#     print(web+str(i+1))
#     scrap(web+str(i+1))

# scrap(web)

            

def vea_category(web):
    
    for i in range(100):
        print(i)
        success = scrap((web[0]+str(i*48)+web[1]+str((i+1)*48)))
        print(web[0]+str(i*48)+web[1]+str((i+1)*48))
        # if success == True:
        #     continue
     
        # if success == True:
        #    continue
        
        # if success == False:
        #     return False
     


array_tec=[]

#arg_ = sys.argv[1]
num = sys.argv[1]
arg_ = config("VEA_TEXT_PATH")+str(num)+".txt"

f = open(arg_, "r")


for i in f:
    array_tec.append(i.split()) 
count = len(array_tec)

print(array_tec)

def vea_scrapper():
  try:
    for id, val in enumerate(array_tec):

        web = val
        success = vea_category(web) ## GENERA LA LISTA DE PAGINACIONES POR CATEGORIA
        print("esta web es la numero "+str(id+1)+" de aprox 500")

        if success == False:
            continue
        if id == count-1:
            print("se acabo la web y va comenzar a dar vueltas")
            time.sleep(10)
            
            vea_scrapper() 
  except:
    vea_scrapper()
        
vea_scrapper()











    