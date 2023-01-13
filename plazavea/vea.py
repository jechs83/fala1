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

web = "https://www.plazavea.com.pe/api/catalog_system/pub/products/search?fq=C:/678/&_from=21&_to=41&O=OrderByScoreDESC&"
def scrap (web):

    proxies = {"http":"http://"+web_ram }
    #res=requests.get(web,  proxies= proxies)
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
        print()
        print(brand)
        print(product)
        print(sku)
        print(link)
        print(image)
        print(list_price)
        print()
        print(dsct)
        print(best_price)
        print(stock)
        
        bd_name_store = "plaza"
            # collection = "market"  #   NOMBRE DE BASE DE DATOS
        market = "vea"    # COLECCION
        card_dsct = 0
        card_price = 0
        date_time = load_datetime()

        save_data_to_mongo_db(bd_name_store, market,sku,brand,product,list_price,
                                best_price,card_price,link,image,dsct, card_dsct, date_time[0] ,date_time[1])
        print("graba")
    print("termino")
        


# for i  in range (500):
#     print(web+str(i+1))
#     scrap(web+str(i+1))

scrap(web)

            

# # web = open(config("VEA_TEXT_PATH"),"r").readlines()
# # links = []
# # for url in web:
  
# #     links.append(url.rstrip())



# # webs = []
# # for i,v in enumerate(links):
# #     for e in range (200):

# #         a=v+str(e+1)
 
# #         webs.append(a)



# # # def vea_scrapping ():

# # #     for id, val  in enumerate (webs):

# # #         scrapping = scrap(val)
# # #         print(scrapping)
# # #         print(val)
# # #         if scrapping == False:
# # #             continue
        
     
                
            
# # # vea_scrapping() 

# # scrap("https://www.plazavea.com.pe/api/catalog_system/pub/products/search?fq=C:/678/683/&_from=1&_to=20&O=OrderByScoreDESC&")