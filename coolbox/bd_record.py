from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from decouple import config
from datetime import datetime

client = MongoClient(config("MONGO_DB"))

def dia():
    now = datetime.now()
    date = now.strftime("%d/%m/%Y")
    time = now.strftime("%H:%M:%S")
    return date, time

def save_data_to_mongo_db(bd_name_store, collection, market, sku, brand, product, list_price,
                            best_price, card_price, link, image, dsct, card_dsct, current_date, current_time, web):

    db = client[bd_name_store]
    collection = db[collection]

    data = {
        "_id": market + sku,
        "sku": sku,
        "market": market,
        "brand": str(brand),
        "product": str(product),
        "list_price": float(list_price),
        "best_price": float(best_price),
        "card_price": float(card_price),
        "web_dsct": float(dsct),
        "card_dsct": float(card_dsct),
        "link": str(link),
        "image": str(image),
        "date": current_date,
        "time": current_time,
        "home_list": web
    }

    try:
        # Use update_one with upsert=True to insert or update the document
        collection.update_one({"_id": market + sku}, {"$set": data}, upsert=True)
    except DuplicateKeyError as e:
        # Handle the duplicate key error here (e.g., log it)
        pass
