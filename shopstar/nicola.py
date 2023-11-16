from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by  import By 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        #options.add_argument("--log-level=3") 
        # Provide the path to the chromedriver executable
        driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
        driver.implicitly_wait(20) # gives an implicit wait for 20 seconds
    
        print("prueba")
        driver.get(web)
        
       
        # Find the SVG element using its class name
       # Find the section containing the button
        section = driver.find_element(By.CLASS_NAME, "sc-1mo03og-0")

        # Find the "OK" button within the section
        ok_button = section.find_element(By.CLASS_NAME, "sc-1fvy7wj-0")
       

        # Click on the "OK" button
        ok_button.click()    
        time.sleep(5)

     
        driver.switch_to.frame(0)
        wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed
        element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".answer:nth-child(1) .image")))

        # Click on the element
        element.click()
        time.sleep(1)
        # Click on the element

        driver.close
        print("hizo u click")
    
   
       

for i in range (200000):
    print(i+1)
    try:
     scrap(web)
    except:
        scrap(web)
    time.sleep(1)
