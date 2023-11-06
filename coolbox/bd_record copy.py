
from pymongo import MongoClient
from decouple import config
client = MongoClient(config("MONGO_DB"))
from datetime import datetime

def dia():
    now = datetime.now()
    date = now.strftime("%d/%m/%Y")
    #date = date.today()
    time = now.strftime("%H:%M:%S")
    return date, time

def save_data_to_mongo_db(bd_name_store,collection, market,sku,brand,product,list_price,
                            best_price,card_price,link,image,dsct, card_dsct, current_date, current_time, web):

        db = client[bd_name_store]
        collection = db[collection]
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
            "date":dia()[0],
              "time":dia()[1],
            "home_list":web
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
              "time":current_time,
            "home_list":web
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
              "time":current_time,
            "home_list":web
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
              "time":current_time,
            "home_list":web
            }
            collection_max.insert_one(data)
       
