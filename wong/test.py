import sys
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime
import os
import json
import random
from datetime import date
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from decouple import config
current_time= time.strftime("%H:%M")
date = date.today()
current_day= date.strftime("%d/%m/%Y")


web_url = random.choice(config("PROXY"))
client = MongoClient(config("MONGO_DB"))

web = "https://www.wong.pe/electrohogar/cocina"


import re
import urllib.request
response = urllib.request.urlopen(web)
html = response.read()
text = html.decode()
re.findall('(.*?)',text)