import matplotlib.pyplot as plt
import pandas as pd
from pymongo import MongoClient
import os
import pymongo
import mpld3
from decouple import config
import pandas as pd
import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

client = MongoClient(config("MONGO_DB"))
db5 = client["scrap"]
collection5 = db5["scrap"] 



def minimo(sku):
    price_list = []
    

    #cod = collection5.find({"sku":str(sku)}).sort("date", pymongo.DESCENDING)
    cod = collection5.aggregate([{'$match': {'sku': str(sku)}}, {'$addFields': {'dateObject': {'$dateFromString': {'dateString': '$date', 'format': '%d/%m/%Y'}}}}, {'$sort': {'dateObject': pymongo.ASCENDING}}])

    for i in cod:
        price_list.append(i["best_price"])
    
    number_list = [float(x) for x in price_list]
    print(number_list)
    min_price = min(number_list)
    print("#######")
    print(min_price)
    last_price = price_list[-1]



    if len(set(price_list)) == 1:
        print("All prices in the list are the same.")
        return False

    else:
    
        if last_price == min_price:
            print("The last price in the list is the historic minimum.")
            print(last_price)
            max_value = max(price_list)
            prev_price = price_list[-2]
           
            return last_price, prev_price,max_value, True
        else:
            print("The last price in the list is not the historic minimum.")

            return False
    
        
minimo("18377775")