
from pymongo import MongoClient
from decouple import config
client = MongoClient(config("MONGO_DB"))


def save_data_to_mongo_db(bd_name_store,collection, market,sku,brand,product,list_price,
                            best_price,card_price,link,image,dsct, card_dsct, current_date):

        db = client[bd_name_store]
        collection = db[collection]
        db_max = client["scrap"]
        collection_max = db_max["scrap"]

        x = collection.find_one({"product":product})
        y = collection_max.find_one({"product":product})
        
        if x  :
            #print(" ACTUALIZA BASE DE DATOS ")
            filter = {"product":product}
            newvalues = { "$set":{ 
          
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
          
            }}
            collection.update_one(filter,newvalues)            
        else:
            
            data =  {
    
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
          
            }
            collection.insert_one(data)
            
        if y :
            #print(" ACTUALIZA BASE DE DATOS ")
            filter = {"product":product}
            newvalues = { "$set":{ 
         
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

            }}
           
            collection_max.update_one(filter,newvalues)
        else:
            
            data =  {
        
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
  
            }
            collection_max.insert_one(data)
       
