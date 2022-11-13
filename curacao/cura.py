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
server_date = datetime.now()
timezone = pytz.timezone("America/Bogota")
peru_date = server_date.astimezone(timezone)
current_date = peru_date.strftime("%d/%m/%Y" )
current_time =peru_date.strftime("%H:%M" )

web_url = random.choice(config("PROXY"))
web_url = "http://"+web_url

client = MongoClient(config("MONGO_DB"))


print(web_url)
 

def scrap (web):
 
    proxies = {"http":web_url }
    #res=requests.get(web,  proxies= proxies)
    HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

    
    res = requests.get(web, proxies={"http": web_url}, headers = HEADERS)

    
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
        print(product)
        brand = i.find("div", class_="Manufacturer").text
        print(brand)
        try:
            sku = i.find("div" ,class_="PartNumber" ).text
            sku = sku.replace("_P","")
        except: sku = None
        
        link = i.find("a")["href"]
        print(link)

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
        market = "curacao"
        
        db = client["curacao"]
        collection = db["market"]
        db_max = client["scrap"]
        collection_max = db_max["scrap"]

        try:
            card_price = 0
        except:card_price=0
        #print(card_price)
        bd_name_store = market
        dsct = web_dsct

        card_dsct = 0
        save_data_to_mongo_db(bd_name_store, market,sku,brand,product,list_price,
                            best_price,card_price,link,image,dsct, card_dsct)
        

# def scrap_category(web1,web2,count):
#     for i in range(500):
       
#         success = scrap(web1+str((i+1)*count)+web2)
#         print(web1+str((i+1)*count)+web2)
#         #time.sleep(3)
#         if success == True:
#             print("succes es Verdadero ")
#             return False

array_tec=[]

#arg_ = sys.argv[1]
num = sys.argv[1]
arg_ = config("CURACAO_TEXT_PATH")+str(num)+".txt"

f = open(arg_, "r")
x = f.readlines()

with open(arg_) as load_file:
    data = [tuple(line.split()) for line in load_file]



# for id, val in enumerate(data):
    
#         count = 12
#         web1 = val[0]
#         #web2=val[1]
#         web2 = "&pageSize=12&pageGroup=Category&urlLangId=-24"
        
#         scrap_category(web1,web2,count) ## GENERA LA LISTA DE PAGINACIONES POR CATEGORIA
#         if scrap_category == False:
#             continue


counter =len(array_tec)
def curacaro_scrap():

    for id, val in enumerate(data):
        
            count = 12
            web1 = val[0]
            #web2=val[1]
            web2 = "&pageSize=12&pageGroup=Category&urlLangId=-24"

            for i in range(500):
       
                success = scrap(web1+str((i+1)*count)+web2)
                print(web1+str((i+1)*count)+web2)
                #time.sleep(3)
                if success == True:
                    print("se termino pahginacion")
                    break

            if id == counter-1:
                print("se acabo la web y va comenzar a dar vueltas")
                time.sleep(5)
                
                curacaro_scrap()
        

curacaro_scrap()





         







    