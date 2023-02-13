import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import sys
from datetime import datetime
import random
import gc
import time
import json

from datetime import datetime
from datetime import date

from decouple import config
import subprocess
text_file = open(config("PROXY"), "r")
lines = text_file.readlines() 
web_url = random.choice(lines)
client = MongoClient(config("MONGO_DB"))


bd_name = "saga"
collection_status = "status"  #   NOMBRE DE BASE DE DATOS
db1 = client[bd_name]
collection1 = db1[collection_status]

lista =[100,111,112,113,114,115,116]
  
for i, v in enumerate(lista):

        
    subprocess.Popen(["start", "C:\GIT\\fala\\ripley\\as.py", str(v)] ,shell=True, executable="C:\WINDOWS\system32\cmd.exe")
    time.sleep(10)
         
        
        
    



    
    
    

