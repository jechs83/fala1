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





def url(): 
        chrome_driver_path =  "/Users/javier/GIT/fala/buscador/chromedriver"

         # Test name: registrio
        # Step # | name | target | value
        # 1 | open | /falabella-pe/myaccount/registration | 
        options = Options()
        #options.add_argument('--headless')
        #options.add_argument('--window-size=1920,1080')
        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        except:
            driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

        driver.implicitly_wait(20) # gives an implicit wait for 20 seconds
        driver.get("https://www.falabella.com.pe/falabella-pe")
        # 2 | setWindowSize | 1680x951 | 
        #driver.set_window_size(1680, 951)
        # 3 | click | id=testId-Input-firstName | 
        time.sleep(5)
        # Find the "No, gracias" button by its data attribute
        driver.find_element(By.CSS_SELECTOR, ".MarketplaceHamburgerBtn-module_icon__YC2PL").click()
        categoria =["Electrohogar", "Tecnología","Mujer", "Hombre"]

    
            
        driver.find_element(By.XPATH,'//div[text()="Electrohogar"]').click()

        li_elements = driver.find_elements(By.TAG_NAME,"li")

        # Extract and print the URLs
        for li in li_elements:
            
                link = li.find_element(By.TAG_NAME, "a")
                url = link.get_attribute("href")
                if url:
                    print(url)
        
        time.sleep(2)
        driver.find_element(By.CLASS_NAME,"TaxonomyDesktop-module_closeIcon__2X3P0").click()
        driver.find_element(By.CSS_SELECTOR, ".MarketplaceHamburgerBtn-module_icon__YC2PL").click()


        driver.find_element(By.XPATH,'//div[text()="Tecnología"]').click()

        li_elements = driver.find_elements(By.TAG_NAME,"li")
        li_elements = driver.find_elements(By.TAG_NAME,"li")

        # Extract and print the URLs
        for li in li_elements:
            
                link = li.find_element(By.TAG_NAME, "a")
                url = link.get_attribute("href")
                if url:
                    print(url)
        

     

    
  

url()
     

#register_safa("pedro","palote",999999999,"pablssso@gmail.com")


    # do something with the data here
    # for example, print the first five rows



