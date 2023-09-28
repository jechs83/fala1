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
import sys
import pandas as pd
import random
from fake_useragent import UserAgent


# Create a UserAgent object to generate random user agents
user_agent = UserAgent()

# Generate a random user agent
random_user_agent = user_agent.random
cat = ["televisores", "celulares_fijos","laptops","computacion_gamer","videojuegos_entretenimiento","audio_para_tv","fotografia_entretenimiento","smart_home"]
cat2 =["perfumeria","tratamiento_bell","belleza_dermocosmetica","maquillaje","cuidado_capilar","bellez_nuev_cuida_personal","belle_homb","belle_acc","belle_marc"]
        

def url(cat): 
        chrome_driver_path =  "/Users/javier/GIT/fala/buscador/chromedriver"
        options = Options()     
        #custom_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

        options.add_argument(f"user-agent={random_user_agent}")
        
        #options.add_argument('--headless')
        #options.add_argument('--window-size=1920,1080')
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        except:
            driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

        # driver.implicitly_wait(20) # gives an implicit wait for 20 seconds
        # driver.get("https://simple.ripley.com.pe/")
        # driver.set_window_size(1680, 944)
        # menu = driver.find_element(By.CSS_SELECTOR, ".menu-button__icon").click()

        
       


        cat_prin = ["category-item-belleza","","","","","","","","",""]

        for i,v  in enumerate(cat_prin):

            driver.implicitly_wait(20) # gives an implicit wait for 20 seconds
            driver.get("https://simple.ripley.com.pe/")
            driver.set_window_size(1680, 944)
            
            menu = driver.find_element(By.CSS_SELECTOR, ".menu-button__icon").click()

            driver.find_element(By.CSS_SELECTOR, "."+v).click()
            
            for i,v in enumerate(cat):
                driver.find_element(By.ID, v).click()
                current_url = driver.current_url
                print(current_url)
            
                element = driver.find_element(By.XPATH,"//div[contains(@class, 'col-xs-12 col-md-9 col-lg-9')]")
                number_products = element.text
            
                print(number_products.split()[0])
                driver.find_element(By.CLASS_NAME,"menu-button__icon").click()

                time.sleep(2)
            driver.find_element(By.CLASS_NAME,"tree-node-back-button").click
            # driver.quit()



    


        

url(cat2)
     

#register_safa("pedro","palote",999999999,"pablssso@gmail.com")


    # do something with the data here
    # for example, print the first five rows



