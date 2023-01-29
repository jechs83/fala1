import time
import os
import subprocess 
from pymongo import MongoClient
from decouple import config

client = MongoClient(config("MONGO_DB"))





def urls_list( id):

    db = client["saga"]
    collection = db["lista"]
    
    x = collection.find({"_id":int(id)})
    for i in x:
        list = i["url"]
    return list

    


    # if x  :
    #         #print(" ACTUALIZA BASE DE DATOS ")
    #     filter = {"_id":int(id)}
    #     newvalues = { "$set":{ 
    #     "status":bd_status, 
    #     }}
    #     collection.update_one(filter,newvalues)      

urls_list("lista", 1)
    