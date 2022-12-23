
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


def save_data_to_mongo_db( sku,brand,product,list_price,
                            best_price,card_price,link,image,dsct,db_collection):

        
        
        db = client["scrap"]
        collection = db[db_collection]

        x = collection.find_one({"_id":sku})
      
    
        if x  :
            #print(" ACTUALIZA BASE DE DATOS ")
            filter = {"_id":sku}
            newvalues = { "$set":{ 
            "_id":sku,   
            "sku":sku, 
            "brand":str(brand),
            "product": str(product),
            "list_price":float(list_price),
            "best_price":float(best_price),
            "card_price": float(card_price),
            "web_dsct":float(dsct),
            "link": str(link),
            "image": str(image),
            "telegram":"search"
            }}
            collection.update_one(filter,newvalues)
 
            
        else:
            
            data =  {
            "_id":sku,     
            "sku":sku, 
            "brand":str(brand),
            "product": str(product),
            "list_price":float(list_price),
            "best_price":float(best_price),
            "card_price": float(card_price),
            "web_dsct":float(dsct),
            "link": str(link),
            "image": str(image),
            "telegram":"search"
            }
            collection.insert_one(data)
          
            
       