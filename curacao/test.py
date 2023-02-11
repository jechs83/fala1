
from pymongo import MongoClient
from decouple import config
import datetime
from datetime import datetime
from datetime import date
import datetime

client = MongoClient(config("MONGO_DB"))


db = client["scrap"]
collection = db["scrap"]


def load_datetime():
    
 today = date.today()
 now = datetime.now()
 date_now = today.strftime("%d/%m/%Y")  
 time_now = now.strftime("%H:%M:%S")
 return date_now, time_now


now = datetime.datetime.now()
print(now)
x = collection.find_one({"sku":"2019263720455P" } )
# from datetime import datetime

# time_string = "14:30:00"
# time_format = "%H:%M:%S"

# time_object = datetime.strptime(time_string, time_format)

# print(time_object)