
from pymongo import MongoClient
import os
import sys
import time
from decouple import config
import subprocess

client = MongoClient(config("MONGO_DB"))
db = client["scrap"]

collection = db["scrap"]

product_array = []
    
    

t1 =  collection.find( {"web_dsct":{ "$gte":50, "$not":{"$gte":101}},"date":"10/02/23" , "product":{"$not":{"$in":[re.compile(producto,re.IGNORECASE),re.compile("reloj",re.IGNORECASE) ]} } })

   

for i in t1:
        product_array.append(i)
        #print(i)


collection_1 = db["excelsior1"]
collection_2 = db["excelsior2"]


for i in 

a= collection_1.find({"sku":i["sku"]})
# se busca datos en offer1 cada iteracion
#a=list(a)

b= collection_2.find({"sku":i["sku"]})
# se busca datos en offer2  en cada iteracion 
#b = list(b)

if a.all()
#print(b)
#len_b = len(b)
#print(len_b)
b_len = len(b)
