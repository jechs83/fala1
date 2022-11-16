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
from datetime import datetime
from datetime import date

def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now


from decouple import config
web_url = random.choice(config("PROXY"))

client = MongoClient(config("MONGO_DB"))


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
    try:
     x = js["props"]["pageProps"]["results"]
    except: return False

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
        if sku ==0:
            continue

        



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
        print()
        print( "producto numero "+ str(i+1));
        print(sku);print(brand);print(product);print("list price "+str(list_price));print("best price "+str(best_price));print("card price "+str(card_price));
        print("descuento "+str(web_dsct)); print("link "+link)
        
        # db = client["saga"]
        # collection = db["market"]
        # db_max = client["scrap"]
        # collection_max = db_max["scrap"]
        

        bd_name_store = "saga"  #   NOMBRE DE BASE DE DATOS
        market = "saga_test"    # COLECCION
        dsct = web_dsct
        card_dsct = 0
        date_time = load_datetime()
        save_data_to_mongo_db(bd_name_store, market,sku,brand,product,list_price,
                            best_price,card_price,link,image,dsct, card_dsct, date_time[0] ,date_time[1])

        # t = collection.find_one({"_id":market+str(sku)})
        # y = collection_max.find_one({"_id":market+str(sku)})
        
        # if t :
        #     #print(" ACTUALIZA BASE DE DATOS ")
        #     filter = {"_id":market+str(sku)}
        #     newvalues = { "$set":{ 
        #     "_id":market+str(sku),   
        #     "sku":sku, 
        #     "market":market,
        #     "brand":str(brand),
        #     "product": str(product),
        #     "list_price":float(list_price),
        #     "best_price":float(best_price),
        #     "card_price": float(card_price),
        #     "web_dsct":float(web_dsct),
        #     "link": str(link),
        #     "image": str(image),
        #     "date":current_date,
        #     "time":current_time
        #     }}
        #     collection.update_one(filter,newvalues)
        #     collection_max.update_one(filter,newvalues)
                    
        # else:     
        #     data =  {
        #     "_id":market+str(sku),     
        #     "sku":sku, 
        #     "market":market,
        #     "brand":str(brand),
        #     "product": str(product),
        #     "list_price":float(list_price),
        #     "best_price":float(best_price),
        #     "card_price": float(card_price),
        #     "web_dsct":float(web_dsct),
        #     "link": str(link),
        #     "image": str(image),
        #     "date":current_date,
        #     "time":current_time
        #     }
        #     collection.insert_one(data)
    
    
        # if y :
        #     #print(" ACTUALIZA BASE DE DATOS ")
        #     filter = {"_id":market+str(sku)}
        #     newvalues = { "$set":{ 
        #     "_id":market+str(sku),   
        #     "sku":sku, 
        #     "market":market,
        #     "brand":str(brand),
        #     "product": str(product),
        #     "list_price":float(list_price),
        #     "best_price":float(best_price),
        #     "card_price": float(card_price),
        #     "web_dsct":float(web_dsct),
        #     "link": str(link),
        #     "image": str(image),
        #     "date":current_date,
        #     "time":current_time
        #     }}  
        #     collection_max.update_one(filter,newvalues)
                    
        # else:    
        #     data =  {
        #     "_id":market+str(sku),     
        #     "sku":sku, 
        #     "market":market,
        #     "brand":str(brand),
        #     "product": str(product),
        #     "list_price":float(list_price),
        #     "best_price":float(best_price),
        #     "card_price": float(card_price),
        #     "web_dsct":float(web_dsct),
        #     "link": str(link),
        #     "image": str(image),
        #     "date":current_date,
        #     "time":current_time
        #     }
    
        #     collection_max.insert_one(data)
    

def scrap_category(category_url):
    for i in range(500):

        success = scrap(category_url+str(i+1))
        print(category_url+str(i+1))
        #time.sleep(3)
        if success == False:
            return


array_tec=[]

#arg_ = sys.argv[1]
num = sys.argv[1]
arg_ = config("SAGA_TEXT_PATH")+str(num)+".txt"

f = open(arg_, "r")
x = f.readlines()

for i in x:
    array_tec.append(i.rstrip()) 

count = len(array_tec)

def saga_scrapper():
    
    for id, val in enumerate(array_tec):
        print(val)
    
        web = val
        
        scrap_category(web) ## GENERA LA LISTA DE PAGINACIONES POR CATEGORIA
        print("esta web es la numero "+str(id+1)+" de aprox 500")


        if id == count-1:
            print("se acabo la web y va comenzar a dar vueltas")
            time.sleep(10)
            
            saga_scrapper() 
        



saga_scrapper()








    