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


def scrap (web):


    proxies = {"http":"http://"+web_url }
        
    res=requests.get(web,  proxies= proxies)
    print("Respuesta del servidor :"+str(res.status_code))



    soup = BeautifulSoup(res.text, "html.parser")
    
    error = soup.find( "h3" , class_="jsx-860724461")
    print()
    print(error)
    print()
    if error:
        return False
   
    data = soup.find("script", id="__NEXT_DATA__" ).text

   
        

    #data= soup.find_all("div", class_="jsx-3128226947")
    js = json.loads(data)

    with open("/Users/javier/GIT/fala/falabella/source.txt", "w+") as b:
        b.write(data)
        b.close


    x = js["props"]["pageProps"]["results"]

    #print(x[0]["productId"])

    for i in range (55):
       
        #productId= x[i]["productId"]
        try:
         brand = x[i]["brand"]
        except: brand= "None"
        try:
         product = x[i]["displayName"]
        except: product= "None"
        try:
         web_dsct = x[i]["discountBadge"]["label"]
         web_dsct = web_dsct.replace("-","").replace("%","")
         
        except: web_dsct =0



        try:
         image = x[i]["mediaUrls"][0]
        except:  
            try:    
             image = x[i]["mediaUrls"]
            except: image = "None"
        try:
         sku = x[i]["skuId"]
        except: sku = 0
        try:
         link = x[i]["url"]
        except: link = "None"
        try:
         card_price = x[i]["prices"][0]["price"][0]
         card_price = card_price.replace(",","")
      
        except: card_price = 0

        try:
         best_price = x[i]["prices"][1]["price"][0]
         best_price = best_price.replace(",","")
 
        except: best_price= 0
        try:
         list_price= x[i]["prices"][2]["price"][0]
         list_price = list_price.replace(",","")
         
        except: list_price = 0 
        try:
         seller = x[i]["sellerName"]
        except: seller = "None"
        market = "saga"
        # print()
        # print( "producto numero "+ str(i+1));
        # print(sku);print(brand);print(product);print("list price "+str(list_price));print("best price "+str(best_price));print("card price "+str(card_price));
        # print("descuento "+str(web_dsct)); print("link "+link)
        
        db = client["tottus"]
        collection = db["market"]
        db_max = client["scrap"]
        collection_max = db_max["scrap"]
        
        

        t = collection.find_one({"_id":market+str(sku)})
        y = collection_max.find_one({"_id":market+str(sku)})
        
        if t :
            #print(" ACTUALIZA BASE DE DATOS ")
            filter = {"_id":market+str(sku)}
            newvalues = { "$set":{ 
            "_id":market+str(sku),   
            "sku":sku, 
            "market":market,
            "brand":str(brand),
            "product": str(product),
            "list_price":float(list_price),
            "best_price":float(best_price),
            "card_price": float(card_price),
            "web_dsct":float(web_dsct),
            "link": str(link),
            "image": str(image),
            "date":current_date,
            "time":current_time
            }}
            collection.update_one(filter,newvalues)
            collection_max.update_one(filter,newvalues)
                    
        else:     
            data =  {
            "_id":market+str(sku),     
            "sku":sku, 
            "market":market,
            "brand":str(brand),
            "product": str(product),
            "list_price":float(list_price),
            "best_price":float(best_price),
            "card_price": float(card_price),
            "web_dsct":float(web_dsct),
            "link": str(link),
            "image": str(image),
            "date":current_date,
            "time":current_time
            }
            collection.insert_one(data)
    
    
        if y :
            #print(" ACTUALIZA BASE DE DATOS ")
            filter = {"_id":market+str(sku)}
            newvalues = { "$set":{ 
            "_id":market+str(sku),   
            "sku":sku, 
            "market":market,
            "brand":str(brand),
            "product": str(product),
            "list_price":float(list_price),
            "best_price":float(best_price),
            "card_price": float(card_price),
            "web_dsct":float(web_dsct),
            "link": str(link),
            "image": str(image),
            "date":current_date,
            "time":current_time
            }}  
            collection_max.update_one(filter,newvalues)
                    
        else:    
            data =  {
            "_id":market+str(sku),     
            "sku":sku, 
            "market":market,
            "brand":str(brand),
            "product": str(product),
            "list_price":float(list_price),
            "best_price":float(best_price),
            "card_price": float(card_price),
            "web_dsct":float(web_dsct),
            "link": str(link),
            "image": str(image),
            "date":current_date,
            "time":current_time
            }
    
            collection_max.insert_one(data)
    
                
       


# array_tec=[]

# arg_=sys.argv[1]

# f = open(arg_, "r")
# x = f.readlines()
# for i in x:
#    array_tec.append(i.rstrip()) 
# f.close
## OBTEGO UNA LISTA DE LAS URLS PARA SCRAPEAR 

def scrap_category(category_url):
    for i in range(500):

        success = scrap(category_url+str(i+1))
        print(category_url+str(i+1))
        #time.sleep(3)
        if success == False:
            return

###########################################################
array_tec=[]
arg_ = sys.argv[1]

f = open(arg_, "r")
x = f.readlines()

for i in x:
    array_tec.append(i.rstrip()) 
# webs= []
# for i,v in enumerate(array_tec):
#     for i in range (3):
#         webs.append(v+(str(i+1)))
# print(webs)

for id, val in enumerate(array_tec):
    print(val)
  
    web = val

    scrap_category(web) ## GENERA LA LISTA DE PAGINACIONES POR CATEGORIA
# x= "https://www.falabella.com.pe/falabella-pe/category/cat760702/Telefonia?page="

# scrap_category(x)









    