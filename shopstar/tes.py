import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import sys
from datetime import datetime
import random
import gc
import time
import json

def dia():
    now = datetime.now()
    date = now.strftime("%d/%m/%Y")
    #date = date.today()
    time = now.strftime("%H:%M:%S")
    return date, time

print(dia()[0])

dia()
    



    
    
    

