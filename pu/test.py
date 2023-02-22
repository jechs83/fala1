import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import sys
from datetime import datetime
import random
import gc
import time
import json
from bd_record import save_data_to_mongo_db
from datetime import datetime
from datetime import date
from multiprocessing import Pool, freeze_support
from decouple import config
import subprocess
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import sys
from datetime import datetime
import pytz
import random
import time
from bd_record import save_data_to_mongo_db
from decouple import config
text_file = open(config("PROXY"), "r")
lines = text_file.readlines() 
from datetime import datetime
from datetime import date
HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

web_url = random.choice(lines)
client = MongoClient(config("MONGO_DB"))


list =[]

for i in range (100000):
      list.append("https://sparxworks.com")

def scrap (web):

    proxies = {"http":"http://"+web_url }
        
    res=requests.get(web,  proxies= proxies, headers=HEADERS)

    print(res.body)
    print("Respuesta del servidor :"+str(res.status_code))


  
def g():

    if __name__ == '__main__':

            freeze_support()
            p = Pool(100)
            p.map (scrap,list)
            p.terminate()
            p.join()
    g()
g()

            
