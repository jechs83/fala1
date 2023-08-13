from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by  import By 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
from bd_record import save_data_to_mongo_db, dia
import re
import sys
from bs4 import BeautifulSoup
from datetime import datetime
import  urls_list 
from decouple import config

from pymongo import MongoClient
import logging

# Set the logging level to WARNING (or higher)
logging.basicConfig(level=logging.CRITICAL)
client = MongoClient(config("MONGO_DB"))
chromedriver_path = config("chromedriver_path")


web = "https://www.lacasadelosfamososmexico.tv/vota/"



def scrap(web): 
        options = Options()
        #options.add_argument('--headless')
        options.add_argument('--window-size=1920,1080')
        driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
        driver.implicitly_wait(20) # gives an implicit wait for 20 seconds
    
        print("prueba")
        driver.get(web)
        
        section = driver.find_element(By.CLASS_NAME, "sc-1mo03og-0")
        # Find the "OK" button within the section
        ok_button = section.find_element(By.CLASS_NAME, "sc-1fvy7wj-0")
        # Click on the "OK" button
        ok_button.click()    
        time.sleep(4)

     
        driver.switch_to.frame(0)
        driver.find_element(By.CSS_SELECTOR, ".answer:nth-child(1) .image").click()
        print("voto por nicola")
        time.sleep(1)
        # Click on the element

        driver.close
 
    
   
       

for i in range (200000):
    print(i+1)
    try:
     scrap(web)
    except:
        scrap(web)
    time.sleep(1)
