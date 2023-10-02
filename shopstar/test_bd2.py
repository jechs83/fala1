from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from decouple import config
from datetime import datetime

client = MongoClient(config("MONGO_DB"))

import pymongo

# Connect to MongoDB

db = client["test1"]
products_collection = db["test1"]

# Define the product ID for which you want to retrieve the historical prices
product_id = 1  # Replace with the actual product ID

# Find the product document by its ID
product = products_collection.find_one({"_id": product_id})

if product:
    # Print the historical prices
    if "price_history" in product:
        for price_entry in product["price_history"]:
            date = price_entry["date"]
            best_price = price_entry["best_price"]
            list_price = price_entry["list_price"]
            card_price = price_entry["card_price"]
            print(f"Date: {date}, Best Price: {best_price}, List Price: {list_price}, Card Price: {card_price}")
    else:
        print("No price history available for this product.")
else:
    print("Product not found.")
