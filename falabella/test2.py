
from pymongo import MongoClient
from decouple import config
client = MongoClient(config("MONGO_DB"))



bd_name_store = "saga"
collection = "status"  #   NOMBRE DE BASE DE DATOS
db = client[bd_name_store]
collection = db[collection]

cursor = collection.find_one({"_id":0})
print(cursor["trigger"])
                                                                            