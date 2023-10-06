
from pymongo import MongoClient
from decouple import config

# Configure the MongoDB connection
MONGODB_URL = config("MONGO_DB")



def compare_prices(MONGO,db, collec,sku,date):
    # Create a MongoDB client
    client = MongoClient(MONGO)

    # Access the database
    db = client[db]

    # Access the collection
    collection = db[collec]


    t1 =  collection.find( {"sku":sku, "date":date })

    prices = collection.find({"sku": sku, "date": {"$ne": date}})

    current_prices = []
    for i in t1:
        current_prices.append((i["list_price"],i["best_price"],i["card_price"]))

    history_price = []
    for i in prices:

        history_price.append((i["list_price"],i["best_price"],i["card_price"]))
    

    for price in current_prices:
    # Iterate through tuples in 'b'
        for h_price in history_price:
            # Check if element_a is lower than any element in the current tuple from 'b'
            if any(price < h_price for h_price in history_price):
                return True
    



if compare_prices(MONGODB_URL,"scrap", "scrap", "PMP0000203423", "05/10/2023") == True:
    print( "precio historico")
