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

    elements=soup.find_all("li", class_="item product product-item")
    if not elements:
        return True
    
    for idx, i in enumerate(elements):
    
        try:
            link=i.find("a", class_="product-item-link").attrs.get("href")
        except: link = None

        try:
            brand=i.find( "div" ,class_="product details product-item-details").find("span", class_="list_item_product_manufacturer").text
        except: brand = "Null"

        try:
            best_price=i.find("div", class_="price-box price-final_price").find("span",class_="price-container price-final_price tax weee").find("span", class_="price").text
            # best_price = best_price[1]
            best_price = best_price.replace("S/","").replace(",","").replace("S/. ","")
            # if best_price != int or float:
            #     best_price=i.find("div", class_="price-box price-final_price").text
            #     best_price = best_price.split()
            #     best_price = best_price[2]
            #     best_price = best_price.replace("S/","").replace(",","").replace("S/. ","")
        except: best_price=0

        try:
            list_price=i.find("div", class_="price-box price-final_price").find("span",class_="old-price").find("span", class_="price").text
            # best_price = best_price[1]
            list_price = list_price.replace("S/","").replace(",","").replace("S/. ","")
            # if best_price != int or float:
            #     best_price=i.find("div", class_="price-box price-final_price").text
            #     best_price = best_price.split()
            #     best_price = best_price[2]
            #     best_price = best_price.replace("S/","").replace(",","").replace("S/. ","")
        except: list_price=0
        # try:
        #     list_price=i.find("span", class_="old-price").find("span,", class_="price").text
        #     list_price = list_price.replace("S/","").replace(",","").replace("S/. ","")
        # except: list_price = 0

        try:
            sku=i.find("div", class_="product-item-inner").find("form").attrs.get("data-product-sku")
        except: sku = 0

        try:
            category=i.find("div").attrs.get("data-category")
        except: category = None

        try:
            product=i.find( "div" ,class_="product details product-item-details").find("a",class_="product-item-link").text
            product = product.strip()
        except: product = None

        try:
            image=i.find( "img", class_="product-image-photo").attrs.get("srcset")
        except: image = None

        try:
         if best_price ==0 and list_price==0 or best_price == list_price:
            web_dsct=0
         else:
            web_dsct= float(list_price)-float(best_price)
            web_dsct = float(web_dsct)*100/float(list_price)
            web_dsct=round(web_dsct,2)
        except:web_dsct = 0

        bd_name_store = "pu"
        collection = "pu"
        market = "pu"
        card_price = 0
        card_dsct =0
        dsct = web_dsct
        date_time = load_datetime()
        # print(),print(brand),print(sku),print(product) ,print(link),print(category),print("LIST PRICE")
        # print(list_price)
        # print("best price")
        # print(best_price)#print(image),print(market),print(web_dsct)

        save_data_to_mongo_db(bd_name_store,collection, market,str(sku),brand,product,list_price,
                            best_price,card_price,link,image,dsct, card_dsct, date_time[0] ,date_time[1])

# def scrapero(web):

#     for i in range(1000):
#         x = shop(web+str(i+1))
#         print(web+str(i+1))
#         if x == True:
#             print(x)
#             return False

#         print("pagina "+str(i+1))


array_tec=[]

num = sys.argv[1]
arg_ = config("PERFUMERIAS_UNIDAS")+str(num)+".txt"

f = open(arg_, "r")
x = f.readlines()

for i in x:
    array_tec.append(i.rstrip())


# for i,v in enumerate(array_tec):

#     scrap =  scrapero(v)

#     if scrap == False:
#         continue
count  = len(array_tec)
def promart_scrap():
    # try:
        for i,v in enumerate(array_tec):
            print(array_tec)

            for e in range(1000):
                x = shop(v+str(e+1))
                print(v+str(e+1))
                # if x == True:
                #  print(x)
                # break

            # if i == count-1:
            #     print("se acabo la web y va comenzar a dar vueltas")
            #     time.sleep(5)
                
            #     promart_scrap()
    # except:
    #     return promart_scrap()

        

promart_scrap()