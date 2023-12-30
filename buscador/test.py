from decouple import config
from pymongo import MongoClient


client = MongoClient(config("MONGO_DB"))
db = client["curacao"]
#collection = db[collection_name]
collection_1 = db["bd1"]

#collection_2 = db[ship_db2]


t = collection_1.find_one({"sku":"SK1019970"})


data_sv = {
                "sku": t["sku"],
                "best_price":t["best_price"],
                "list_price":t["list_price"],
                "card_price":t["card_price"],
                "web_dsct":t["web_dsct"],
                "card_dsct": t["card_dsct"],
   
            }


print(data_sv)
