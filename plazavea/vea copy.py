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
        
    res=requests.get(web,  proxies= proxies)
    print("Respuesta del servidor :"+str(res.status_code))

   
    res=requests.get(web,  proxies= proxies)
    soup = BeautifulSoup(res.text, "html.parser")
    print(soup)

    with open ("/Users/javier/GIT/fala/plazavea/json.txt", "w") as f:
        f.write(str(soup))


    # json_data = json.loads(soup)


    # print(json_data)
scrap(web)
#     lista = []
#     #elements = soup.find("div",class_="ShowcaseGrid")
 
#     elements = soup.find_all("div",class_="Showcase__content")
   
#     for idx,i   in  enumerate (elements):
#         # print(i.text)
#         # time.sleep(20)
        
#         product = (i["title"])
#         product = product.replace("'","")
#         link = i.find("a", class_="Showcase__link").attrs.get("href")
       
#         price = i.find("div", class_="Showcase__priceBox__col").text
#         price = price.split()
#         list_price = price[1].replace(",","")# normal
#         best_price = price[3].replace(",","") # online
#         brand = i.find("div", class_ = "Showcase__brand").text
#         brand = brand.strip()
#         brand = brand.replace("'","")
#         image = i.find("figure", class_="Showcase__photo").find("img").attrs.get("src")

#         try:
#          dsct = round ( (float(best_price)*100/float(list_price)))
#         except: dsct = 0
      
      
#         #print(product)
#         print(list_price)
#         print(best_price)
#         print(dsct)

     
#         market = "vea"    # COLECCION
#         dsct = dsct
#         card_price =0
#         sku = "null"
#         # bd_name_store = "plaza"
#         # collection = "market"  #   NOMBRE DE BASE DE DATOS
#         # date_time = load_datetime()
        
#         card_dsct = 0

#         arr = [{"market":market,
#                 "sku":sku,"brand":brand,
#                 "product":product,
#                 "list_price":str(list_price),
#                  "best_price":str(best_price),
#                  "card_price":str(card_price),
#                  "link":link,
#                  "image":image,
#                  "web_dsct":str(dsct),
#                   "card_dsct":str(card_dsct) 
#                   }]

#         lista.append(arr)
#     lista = str(lista)
#     lista = lista.replace("'",'"').replace("[","").replace("]","")
#     lista = "["+lista+"]"


#     bd_name_store = "plaza"
    
#     collection = "market"  #   NOMBRE DE BASE DE DATOS
#     date_time = load_datetime()
#     db = client[bd_name_store]
#     collection = db[collection]
#     # with open ("/Users/javier/GIT/fala/plazavea/json.txt", "r") as f:
        
#     lista = json.loads(lista)
 
#     collection.insert_many(lista)


# web = "https://www.plazavea.com.pe/api/catalog_system/pub/products/search?fq=C:/678/&_from=84&_to=104&O=OrderByScoreDESC&"
# # for i  in range (500):
# #     print(web+str(i+1))
# #     scrap(web+str(i+1))

# scrap(web)

            

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