from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by  import By 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import pandas as pd
from pymongo import MongoClient
from decouple import config

client = MongoClient(config("MONGO_DB"))
db = client["dni"]
collection = db["dni"]  


query = {"status": 0}
dni = collection.find_one(query)
print(dni["dni"])