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

    cod = collection5.find({"sku":str(sku)})
    for i in cod:
        price_list.append(i["best_price"])
    
    min_price = min(price_list)
    last_price = price_list[-1]

    print(price_list)
    
    if last_price == min_price:
        print("The last price in the list is the historic minimum.")
        print(last_price)
        return True
    else:
        print("The last price in the list is not the historic minimum.")
    
        
    

