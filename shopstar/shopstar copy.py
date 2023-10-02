import sys
import time
from pymongo import MongoClient
import sys
import requests
from bs4 import BeautifulSoup
import re
from bd_record import save_data_to_mongo_db
import time
import random
from decouple import config
from datetime import datetime
from datetime import date
from decouple import config
text_file = open(config("PROXY"), "r")
lines = text_file.readlines() 
import os

web_url = random.choice(lines)
client = MongoClient(config("MONGO_DB"))

def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now


first_sku = None

def shop(web):
    global first_sku
    #headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"}
    proxies = {"http":web_url }

    res=requests.get(web,  proxies= proxies)
    print("Servidor reponde "+str((res.status_code)))
   
    soup = BeautifulSoup(res.text, "html.parser")
    
    elements=soup.find_all("div",class_="product")
    with open ("source.txt", "w+") as f:
       f.write(str(soup))
    print(soup)
    
shop("https://shopstar.pe/tecnologia/televisores?order=OrderByReleaseDateDESC")
#     if not elements:
#         print("no hay elementos")
#         return False
    
#     count=0
#     for idx, i in enumerate(elements):
#         count +=1
#         try:
#          sku= i.find("div", class_="buy-button-normal").attrs.get("id")
#         except:
#             sku = None

#         if  sku == first_sku:
#                 print("se repite SKU")
#                 print(str(sku)+" "+ str(first_sku))
      
#                 return False 

#         if count == 1:
#             first_sku = sku
    

        
#         brand = i.find("h6", class_="x-brand").text
#         product = i.find("h6", class_="x-name").text
#         try:
#          list_price= i.find(class_="product__old-price").text
#          list_price = list_price.replace("S/. ","").replace(",","")
#         except: list_price = 0
#         try:
#          best_price= i.find("span", class_="product__price").text
#          best_price = best_price.replace("S/. ","").replace(",","")
#         except: best_price = 0
       
#         try:
#             web_dsct= i.find(class_="product__discount").text
#             web_dsct= web_dsct.replace("-","").replace(",",".").replace(" %","").replace(" ","")
#             dsct = web_dsct
#         except:  dsct = web_dsct
       

#         try:
#             ibk_dsct = i.find(class_="contentFlag").text
#             ibk_dsct = ibk_dsct.split()[1].replace("%","")
#             card_dsct=float(web_dsct)+float(ibk_dsct)
#             card_dsct=round(card_dsct,2)
#             card_price = (float(best_price)*(100-float(ibk_dsct))/100)
#             card_price = round(card_price,2)
#         except: card_dsct = 0

#         if card_dsct==0:
#             card_price=0

#         try:
#           image = i.find("img").attrs.get("src")
#         except: image = "Null"
#         link = i.find("a").attrs.get("href")
#         category = i.attrs.get("data-cate")
        
#         bd_name_store = "shopstar"
#         collection = "market"  #   NOMBRE DE BASE DE DATOS
#         market = "shopstar"    # COLECCION\
#         date_time = load_datetime()


#         save_data_to_mongo_db(bd_name_store,collection, market,sku,brand,product,list_price,
#                             best_price,card_price,link,image,dsct, card_dsct, date_time[0] ,date_time[1],web)

#         print("product number "+ str(idx+1));print(brand);print(product);print(sku);print(category);print(list_price);print(best_price);print(card_price);
#         print(web_dsct);print(card_dsct);print(link);print("##################");print()



# num = sys.argv[1]
# def urls_list( id):
    
#     db = client["shopstar"]
#     collection = db["lista"]
    
#     x = collection.find({"_id":int(id)})
#     for i in x:
#         list = i["url"]
#     return list
# array_tec = urls_list(num)
# count = len(array_tec)
# print(count)

# db = client["trigger"]
# collection = db["shop"]

# def bd_change(num, bd_status):
    
    
#     x = collection.find_one({"_id":int(num)})
#     if x  :
#             #print(" ACTUALIZA BASE DE DATOS ")
#         filter = {"_id":int(num)}
#         newvalues = { "$set":{ 
#         "status":bd_status, 
#         }}
#         collection.update_one(filter,newvalues)      


# def shop_scrapper():
    
    	
#     for id,v in enumerate(array_tec):
#         print(v)
#         try:
#             for i in range (1000):

#                     if v[-1:] == "=":
#                         url = v+str(i+1)
#                         print(url)
#                     else:
#                         url = v
#                     #print(url)
#                     print(url)
#                     scrap =  shop(url)
                
#                     if scrap == False:
#                         print("salata a la siguiente url")
#                         break
#                     print(id, count-1)
#             if id == count-1:
#                     print("se acabo la web y va comenzar a dar vueltas")
                   
                   
#                     time.sleep(10)
#                     shop_scrapper()
                    
                   
#         except:
#               shop_scrapper()


# shop_scrapper()