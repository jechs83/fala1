
from pymongo import MongoClient
import os
import sys
import time
from decouple import config
import subprocess

client = MongoClient(config("MONGO_DB"))


array2 = ["30", "40", "excelsior" ]


def status_bot(market):
        db = client["trigger"]
        collection = db[market]
        
        x = collection.find_one({"_id":0})
        if x  :
                #print(" ACTUALIZA BASE DE DATOS ")
            filter = {"_id":0}
            newvalues = { "$set":{ 
            "status":2, 
            }}
            collection.update_one(filter,newvalues)   

for idx, val in enumerate(array2):
            
        for i in range (10):
            status_bot(val)