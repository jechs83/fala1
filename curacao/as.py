import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import sys
from datetime import datetime
import random
import gc
import time
import json
from bd_record import save_data_to_mongo_db
from datetime import datetime
from datetime import date
from multiprocessing import Pool, freeze_support
from decouple import config

text_file = open(config("PROXY"), "r")
lines = text_file.readlines() 
web_url = random.choice(lines)
client = MongoClient(config("MONGO_DB"))


def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now

HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

def scrap (web):
     
    proxies = {"http":web_url }
    #res=requests.get(web,  proxies= proxies)
    #HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
    res=requests.get(web,  proxies= proxies, headers=HEADERS)
    
    #res = requests.get(web, proxies={"http": web_url}, proxies = proxies)

    
    server = "Respuesta del servidor :"+str(res.status_code)
    print(server)

    soup = BeautifulSoup(res.text, "html.parser")
    
    product = soup.find_all("li")
    try:
     x = soup.find("div").text
    except: x = None
    if x == None:
        return True
    
    for i in product:

        try:
         product = i.find("a")["title"]
        except: product = None
        print(product)
        brand = i.find("div", class_="Manufacturer").text
        
        print(brand)
        try:
            sku = i.find("div" ,class_="PartNumber" ).text
            sku = sku.replace("_P","")
        except: sku = None
        
        link = i.find("a")["href"]
        #print(link)

        try:
            image = i.find("img")["data-src"]
            image= "https://www.lacuracao.pe"+image
        except: print("none")
        #print(image)
        
        try:
            list_price = i.find("span", class_="old_price").text
            list_price= list_price.strip().replace(",","").replace("S/","")
        except: list_price = 0 
        #print(list_price)
        
        try:
            best_price = i.find("span",  id="offerPriceValue").text
            best_price = best_price.strip().replace(",","")
        except: best_price = 0
        #print(best_price)

        try:
            web_dsct = (float(best_price)*100)/float(list_price)
            web_dsct = (100-web_dsct)

        except: web_dsct = 0
        web_dsct = round( web_dsct)
      
      

        try:
            card_price = 0
        except:card_price=0

        bd_name_store = "curacao"
        collection = "market2"
        dsct = web_dsct
        market = "curacao"
        card_dsct = 0
        date_time = load_datetime()


        save_data_to_mongo_db(bd_name_store,collection, market,sku,brand,product,list_price,
                            best_price,card_price,link,image,dsct, card_dsct, date_time[0] ,date_time[1],web)

        


num = sys.argv[1]
#arg_ = r"C:\\GIT\\fala\\falabella\\urls\\test\\url"+str(num)+".txt"
arg_ = r"/Users/javier/GIT/fala/curacao/urls/link"+str(num)+".txt"
array_tec = []

f = open(arg_, "r")
x = f.readlines()
for i in x:
    #array_tec.append(i.rstrip()) 
    array_tec.append(i.split()) 
        


lista = []
inicio = None





for id, val in enumerate(array_tec):
    if i ==0:
            inicio = load_datetime()
               
    count = 12
    web1 = val[0]
    #web2=val[1]
    web2 = "&pageSize=12&pageGroup=Category&urlLangId=-24"

    for i in range(150):

        scrap(web1+str((i+1)*count)+web2)
    





    if __name__ == '__main__':

            freeze_support()
            p = Pool()
            p.map (scrap,lista)
            p.terminate()
            p.join()
        

print(inicio)
print(load_datetime())


# inicio =None
# for i in range (15):
#     if i == 0:
#      inicio = load_datetime()
#     web = "https://simple.ripley.com.pe/tecnologia/celulares/celulares-y-smartphones?page="+(str(i+1))

#     scrap(web)


# print(inicio)
# print(load_datetime())






    