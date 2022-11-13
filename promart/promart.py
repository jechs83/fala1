import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import sys
from datetime import datetime
import pytz
import random
import time
server_date = datetime.now()
timezone = pytz.timezone("America/Bogota")
peru_date = server_date.astimezone(timezone)
current_date = peru_date.strftime("%d/%m/%Y" )
current_time =peru_date.strftime("%H:%M" )
from decouple import config
from bd_record import save_data_to_mongo_db
web_url = random.choice(config("PROXY"))
client = MongoClient(config("MONGO_DB"))

db = client["shopstar"]
collection = db["promart"]
db_max = client["scrap"]
collection_max = db_max["scrap"]



def shop(web):

    proxies = {"http":"http://"+web_url }

    res=requests.get(web,  proxies= proxies)
    print(res.status_code)
   
    soup = BeautifulSoup(res.text, "html.parser")

    elements=soup.find_all("div", class_="item-product product-listado")

    if not elements:
        return True
    
    for idx, i in enumerate(elements):
    
        try:
            link=i.find("a", class_="prod-det-enlace").attrs.get("href")
           
        except: link = None

        try:
            brand=i.find("div" ,class_="brand js-brand").text
        except: brand = "Null"

        try:
            best_price=i.find("div").attrs.get("data-best-price")
            best_price = best_price.replace("S/ ","").replace(",","").replace("S/. ","")
        except:
            best_price=0
            
        try:
            list_price=i.find("div").attrs.get("data-list-price")
            list_price = list_price.replace("S/ ","").replace(",","").replace("S/. ","")
        except: list_price = 0

        try:
            sku=i.find("div").attrs.get("data-id")
        except: sku = 0

        try:
            category=i.find("div").attrs.get("data-category")
           
        except: category = None


        try:
            product=i.find( "input" ,class_="insert-sku-quantity").attrs.get("title")
            
        except: product = None

        try:
            image=i.find( "img").attrs.get("src")
            
        except: image = None
        try:
         if best_price ==0 and list_price==0 or best_price == list_price:
            web_dsct=0
         else:
            web_dsct= float(list_price)-float(best_price)
            web_dsct = float(web_dsct)*100/float(list_price)
            web_dsct=round(web_dsct,2)
        except:web_dsct = 0

        market = "promart"
        bd_name_store = market
        card_price = 0
        card_dsct =0
        dsct = web_dsct
        print()
        print(brand)
        print(sku)
        print(product) 
        print(link)
        print(category)
        print(list_price)
        print(best_price)
        print(image)
        print(market)
        print(web_dsct)
        save_data_to_mongo_db(bd_name_store, market,sku,brand,product,list_price,
                            best_price,card_price,link,image,dsct, card_dsct)

        # x = collection.find_one({"_id":market+sku})
        # y = collection_max.find_one({"_id":market+sku})

        # if x:
        #         filter = {"_id":market+sku}
        #         newvalues = { "$set":{ 

        #         "_id":market+sku, 
        #         "brand":brand,
        #         "sku":sku,
        #         "market":market,
        #         "product": product,
        #         "list_price":float(list_price),           
        #         "best_price":float(best_price),
        #         "card_price":0,
        #         "web_dsct":web_dsct,
        #         "category":category,
        #         "link": str(link),
        #         "image":str(image),
        #         "date":current_date,
        #         "time":current_time,
        #         }}
        #         collection.update_one(filter,newvalues)
        #         collection_max.update_one(filter, newvalues)
              
        # else:
        #         data =  {
        #         "_id":market+sku, 
        #         "brand":brand,
        #         "sku":sku,
        #         "market":market,
        #         "product": product,
        #         "list_price":float(list_price),           
        #         "best_price":float(best_price),
        #         "card_price":0,
        #          "web_dsct":web_dsct,
        #         "category":category,
        #         "link": str(link),
        #         "image":str(image),
        #         "date":current_date,
        #         "time":current_time,
        #             }
        #         collection.insert_one(data)
        #         collection_max.insert_one(data)
        # if y:
        #         filter = {"_id":market+sku}
        #         newvalues = { "$set":{ 

        #         "_id":market+sku, 
        #         "brand":brand,
        #         "sku":sku,
        #         "market":market,
        #         "product": product,
        #         "list_price":float(list_price),           
        #         "best_price":float(best_price),
        #         "card_price":0,
        #         "web_dsct":web_dsct,
        #         "category":category,
        #         "link": str(link),
        #         "image":str(image),
        #         "date":current_date,
        #         "time":current_time,
        #         }}
            
        #         collection_max.update_one(filter, newvalues)
              
        # else:
        #         data =  {
        #         "_id":market+sku, 
        #         "brand":brand,
        #         "sku":sku,
        #         "market":market,
        #         "product": product,
        #         "list_price":float(list_price),           
        #         "best_price":float(best_price),
        #         "card_price":0,
        #          "web_dsct":web_dsct,
        #         "category":category,
        #         "link": str(link),
        #         "image":str(image),
        #         "date":current_date,
        #         "time":current_time,
        #             }
               
        #         collection_max.insert_one(data)
        


def scrapero(web):

    for i in range(1000):
        x = shop(web+str(i+1))
        print(web+str(i+1))
        if x == True:
            print(x)
            return False

        print("pagina "+str(i+1))


array_tec=[]

#arg_ = sys.argv[1]
num = sys.argv[1]
arg_ = config("PROMART_TEXT_PATH")+str(num)+".txt"

f = open(arg_, "r")
x = f.readlines()
# array_tec=[]
# arg_ = sys.argv[1]
# f = open(arg_, "r")
# x = f.readlines()
for i in x:
    array_tec.append(i.rstrip())


for i,v in enumerate(array_tec):
    scrap =  scrapero(v)

    if scrap == False:
       continue
 
