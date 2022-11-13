
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


def save_data_to_mongo_db(array_page):

        array_page  = str(array_page)


        db = client["saga"]
        collection = db["market"]
        db_max = client["scrap"]
        collection_max = db_max["scrap"]

       
        
  
        collection.insert_many(array_page)
        collection_max.insert_many(array_page)
      
        #collection.insert_many(data)
          
            
      