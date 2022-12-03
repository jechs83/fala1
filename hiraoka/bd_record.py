
from pymongo import MongoClient

from datetime import datetime
import pytz
import random
server_date = datetime.now()
timezone = pytz.timezone("America/Bogota")
peru_date = server_date.astimezone(timezone)
current_date = peru_date.strftime("%d/%m/%Y" )
current_time =peru_date.strftime("%H:%M" )
from decouple import config
web_url = random.choice(config("PROXY"))
client = MongoClient(config("MONGO_DB"))


def save_data_to_mongo_db(bd_name_store, market,sku,brand,product,list_price,
                            best_price,card_price,link,image,dsct, card_dsct,current_date,current_time):

                         
       
        db = client[bd_name_store]
        collection = db["market"]
        db_max = client["scrap"]
        collection_max = db_max["scrap"]

        x = collection.find_one({"_id":market+sku})
        y = collection_max.find_one({"_id":market+sku})
        
   
        if x  :
            #print(" ACTUALIZA BASE DE DATOS ")
            filter = {"_id":market+sku}
            newvalues = { "$set":{ 
            "_id":market+sku,   
            "sku":sku, 
            "market":market,
            "brand":str(brand),
            "product": str(product),
            "list_price":float(list_price),
            "best_price":float(best_price),
            "card_price": float(card_price),
            "web_dsct":float(dsct),
            "card_dsct":float(card_dsct),
            "link": str(link),
            "image": str(image),
            "date":current_date,
            "time":current_time
            }}
            collection.update_one(filter,newvalues)
 
            
        else:
            
            data =  {
            "_id":market+sku,     
            "sku":sku, 
            "market":market,
            "brand":str(brand),
            "product": str(product),
            "list_price":float(list_price),
            "best_price":float(best_price),
            "card_price": float(card_price),
            "web_dsct":float(dsct),
            "card_dsct":float(card_dsct),
            "link": str(link),
            "image": str(image),
            "date":current_date,
            "time":current_time
            }
            collection.insert_one(data)
          
            
            
        if y :
            #print(" ACTUALIZA BASE DE DATOS ")
            filter = {"_id":market+sku}
            newvalues = { "$set":{ 
            "_id":market+sku,   
            "sku":sku, 
            "market":market,
            "brand":str(brand),
            "product": str(product),
            "list_price":float(list_price),
            "best_price":float(best_price),
            "card_price": float(card_price),
            "web_dsct":float(dsct),
            "card_dsct":float(card_dsct),
            "link": str(link),
            "image": str(image),
            "date":current_date,
            "time":current_time
            }}
           
            collection_max.update_one(filter,newvalues)
            
        else:
            
            data =  {
            "_id":market+sku,     
            "sku":sku, 
            "market":market,
            "brand":str(brand),
            "product": str(product),
            "list_price":float(list_price),
            "best_price":float(best_price),
            "card_price": float(card_price),
            "web_dsct":float(dsct),
            "card_dsct":float(card_dsct),
            "link": str(link),
            "image": str(image),
            "date":current_date,
            "time":current_time
            }
          
            collection_max.insert_one(data)
       
