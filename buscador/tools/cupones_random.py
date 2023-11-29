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


def register_cupon2():   
    
    options = Options()
    options.add_argument('--headless')
    webdriver_path = "C:\\Git\\fala\\buscador\\chromedriver.exe"
    #webdriver_path = "//Users//javier//GIT//fala//buscador//chromedriver"
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--user-agent=Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36')
    driver = webdriver.Chrome(service=Service(webdriver_path), options=options)
    driver.implicitly_wait(1) # gives an implicit wait for 20 seconds
    driver.get("http://interbankcupones.pe/rappi")


    query = {"status": 0}
    dni = collection.find_one(query)
    dni = dni["dni"]
    print(dni)

    driver.find_element(By.ID, "document").send_keys(dni)
    time.sleep(0.5)
    driver.find_element(By.ID, "terms").click()
    time.sleep(0.5)
    driver.find_element(By.CLASS_NAME, "form__btn--fullwidth").click()
    try:
        cupon = driver.find_element(By.CLASS_NAME, "form__box-ticket").text
        document_id = "dni"  # Specify the _id of the document to update
        query = {"_id": dni}
        update = {"$set": {"status": 1}}
        result = collection.update_one(query, update)
    except:
        #print("no valido")
        driver.quit()
        return "Dni no valido"
        #cupon = "Dni no valido en cuenta sueldo"
        
    return cupon


