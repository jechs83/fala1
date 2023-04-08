from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by  import By 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys
import pandas as pd




# class Register:
#     def __init__(self):
#         options = Options()
      
#         options.add_argument('--window-size=1920,1080')
#         driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#         driver.implicitly_wait(20) # gives an implicit wait for 20 seconds

def register_safa(name,last_name,dni,cel,email,pwd):    
         # Test name: registrio
        # Step # | name | target | value
        # 1 | open | /falabella-pe/myaccount/registration | 
        options = Options()
        options.add_argument('--headless')
        #options.add_argument('--window-size=1920,1080')
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.implicitly_wait(20) # gives an implicit wait for 20 seconds
        driver.get("https://www.falabella.com.pe/falabella-pe/myaccount/registration")
        # 2 | setWindowSize | 1680x951 | 
        #driver.set_window_size(1680, 951)
        # 3 | click | id=testId-Input-firstName | 
        driver.find_element(By.ID, "testId-Input-firstName").click()
        # 4 | type | id=testId-Input-firstName | ediardo
        driver.find_element(By.ID, "testId-Input-firstName").send_keys(name)
        time.sleep(4)
        # 5 | type | id=testId-Input-lastName | sotelo
        driver.find_element(By.ID, "testId-Input-lastName").send_keys(last_name)
        # 6 | type | id=testId-Input-document | 41630467
        driver.find_element(By.ID, "testId-Input-document").send_keys(dni)
        # 7 | type | id=testId-Input-phoneNumber | 979630207
        driver.find_element(By.ID, "testId-Input-phoneNumber").send_keys(cel)
        driver.execute_script("window.scrollBy(0, 400);")
        # 8 | click | id=testId-Input-email | 
        driver.find_element(By.ID, "testId-Input-email").click()
        # 9 | type | id=testId-Input-email | sr.spo.ck99@gmail.com
        driver.find_element(By.ID, "testId-Input-email").send_keys(email)
        # 10 | click | id=testId-Input-password | 

        driver.find_element(By.ID, "testId-Input-password").click()
        driver.find_element(By.ID, "testId-Input-password").click()
        time.sleep(3)
       
        driver.find_element(By.ID, "testId-Input-password").send_keys(pwd)
        time.sleep(2)

        checkbox = driver.find_element(By.ID,'testId-TyC-BU_consentTemplateRegistroTyC_FAL_PE-checkbox')
        # Click on the checkbox
        checkbox.click()
        checkbox2 = driver.find_element(By.ID,'testId-TyC-ECO_consentTemplateRegistroCMRPuntosTyC_FAL_PE-checkbox')
        checkbox2.click()
        time.sleep(2)

        driver.find_element(By.ID, "testId-Button-submit").click()
        time.sleep(2)

        driver.quit()

     




    # do something with the data here
    # for example, print the first five rows



