from pymongo import MongoClient
from decouple import config

client = MongoClient(config("MONGO_DB"))
db = client["dni"]

def text_todni():
    with open('//Users//javier//GIT//fala//buscador//dnis_valido.txt', 'r') as file:
        lines = file.readlines()

    collection = db["dni"]
    for line in lines:
        record = {
            "_id": line.strip(),
            "dni": line.strip(),
            "status":0
        }
        
        existing_doc = collection.find_one({"_id": line.strip()})
        if existing_doc:
            continue  # Skip insertion if document with the same _id already exists

        collection.insert_one(record)

    client.close()




def reste_dnis():

    client = MongoClient(config("MONGO_DB"))
    db = client["dni"]
    collection = db["dni"]

    query = {}  # Empty query matches all documents
    update = {"$set": {"status": 0}}

    result = collection.update_many(query, update)
    print(f"Number of documents updated: {result.modified_count}")

    client.close()

