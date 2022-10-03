import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import sys
from datetime import datetime
import pytz
import random
import time
import json
from g_var import mongo_db, proxies
server_date = datetime.now()
timezone = pytz.timezone("America/Bogota")
peru_date = server_date.astimezone(timezone)
current_date = peru_date.strftime("%d/%m/%Y" )
current_time =peru_date.strftime("%H:%M" )
client = MongoClient(mongo_db)
web_url = random.choice(proxies)
client = MongoClient(mongo_db)
 
web = "https://www.lacuracao.pe/webapp/wcs/stores/servlet/CategoryNavigationResultsGridScrollView?facet=&totalRows=3&env_resultsPerRow=4&searchTerm=&manufacturer=&filterTerm=&facet=&metaData=&searchType=&categoryId=3074457345616676988&storeId=10151&catalogId=3074457345616676668&orderBy=&minPrice=&maxPrice=&beginIndex=24&pageSize=12&pageGroup=Category&urlLangId=-24"

def scrap (web):
 
    proxies = {"http":"http://"+web_url }
        
    res=requests.get(web,  proxies= proxies)
    server = "Respuesta del servidor :"+str(res.status_code)
    print(server)

    soup = BeautifulSoup(res.text, "html.parser")
    
    product = soup.find_all("li")

    for i in product:
        product = i.find("a")["title"]
        print(product)
        brand = i.find("div", class_="Manufacturer").text
        print(brand)
        sku = i.find("div" ,class_="PartNumber" ).text
        sku = sku.replace("_P","")
        print(sku)

        try:
            image = i.find("img")["data-src"]
            image= "https://www.lacuracao.pe"+image
        except: print("none")
        print(image)
        
        try:
            list_price = i.find("span", class_="old_price").text
            list_price= list_price.strip().replace(",","").replace("S/","")
        except: list_price = 0 
        print(list_price)
        
        try:
            best_price = i.find("span",  id="offerPriceValue").text
            best_price = best_price.strip().replace(",","")
        except: best_price = 0
        print(best_price)

        try:
            web_dsct = (float(best_price)*100)/float(list_price)
        
        except: web_dsct = 0
        print(round( web_dsct))


scrap(web)