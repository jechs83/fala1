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
from decouple import config
from datetime import datetime
from datetime import date

web_url = random.choice(config("PROXY"))
web_url = "http://"+web_url
client = MongoClient(config("MONGO_DB"))


print(web_url)
 
def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now

def scrap (web):
 
    proxies = {"http":web_url }
    #res=requests.get(web,  proxies= proxies)
    #HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
    res=requests.get(web,  proxies= proxies)
    
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

    
        product = i.find("a")["title"]
        #print(product)
        brand = i.find("div", class_="Manufacturer").text
        
        #print(brand)
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
        collection = "market"
        dsct = web_dsct
        market = "curacao"
        card_dsct = 0
        date_time = load_datetime()


        save_data_to_mongo_db(bd_name_store,collection, market,sku,brand,product,list_price,
                            best_price,card_price,link,image,dsct, card_dsct, date_time[0] ,date_time[1])

        

num = sys.argv[1]
arg_ = config("CURACAO_TEXT_PATH")+str(num)+".txt"

f = open(arg_, "r")
x = f.readlines()

with open(arg_) as load_file:
    data = [tuple(line.split()) for line in load_file]

counter =len(data)
print(counter)
def curacaro_scrap():

    for id, val in enumerate(data):
        
            count = 12
            web1 = val[0]
            #web2=val[1]
            web2 = "&pageSize=12&pageGroup=Category&urlLangId=-24"

            for i in range(500):
       
                success = scrap(web1+str((i+1)*count)+web2)
                if i == 1:

                         current_url = web1+str((i+1)*count)+web2
                         print(current_url)
                #time.sleep(3)
                if success == True:
                    print("se termino paginacion continua con la siguiente ")
                    break
            

            if id == counter-1:
                print("se acabo la web y va comenzar a dar vueltas")
                time.sleep(5)
                
                curacaro_scrap()
        

curacaro_scrap()





         







    