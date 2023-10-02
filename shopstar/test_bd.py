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


# Connect to MongoDB
db = client["test1"]
products_collection = db["test1"]



# Define the product ID for which you want to add a historic price
product_id = 1  # Replace with the actual product ID

# Define the new price values
best_price = 201
list_price = 146
card_price = 99
date = "10-01-2023"

# Get the current date
current_date = datetime.now().strftime("%Y-%m-%d")

# Create a historic price document
historic_price = {
    
    "best_price": best_price,
    "list_price": list_price,
    "card_price": card_price,
}

# Try to update the product document by appending the historic price to the price_history array
# If the product document doesn't exist, create a new one
update_result = products_collection.update_one(
    {"_id": product_id, "date": date},
    {"$push": {"price_history": historic_price},
     "$setOnInsert": {
         "best_price": best_price,
         "list_price": list_price,
         "card_price": card_price
     }},
    upsert=True  # Create a new document if it doesn't exist
)

if update_result.upserted_id is not None:
    print("New product document created with historic price.")
elif update_result.modified_count == 1:
    print("Historic price added to an existing product.")
else:
    print("Failed to update or create the product document.")
