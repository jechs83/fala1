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

# #options.add_argument('--headless')
# options.add_argument('--window-size=1920,1080')
# #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install(), options=options ))
# #driver = webdriver.Chrome(executable_path=r"/Users/javier/GIT/Selenium_urls/chromedriver", options = options)
# driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
# driver.get("https://publisherstest.sparxworks.com/app/#/security/login")
# driver.implicitly_wait(20) # gives an implicit wait for 20 seconds



# def register_cupon(dni):    
#         options = Options()
#         options.add_argument('--headless')
#         options.add_argument('--window-size=1920,1080')
#         driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#         chrome_options = Options()
#         driver.implicitly_wait(20) # gives an implicit wait for 20 seconds


#         chrome_options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')
#         driver = webdriver.Chrome(options=chrome_options)

#         driver.get("http://interbankcupones.pe/rappi")
    
#         #driver.set_window_size(1680, 951)

#         driver.find_element(By.ID, "document").send_keys(dni)
#         time.sleep(2)
#         driver.find_element(By.ID, "terms").click()
#         time.sleep(1)
#         driver.find_element(By.CLASS_NAME, "form__btn--fullwidth").click()
#         cupon = driver.find_element(By.CLASS_NAME, "form__box-ticket").text
#         print(cupon)
#         time.sleep(2)
#         return cupon
#         driver.quit()

     


with open("/Users/javier/GIT/fala/buscador/dnis.txt", 'r') as file:
    lines = file.readlines()
    dni = random.choice(lines).strip()

   


def register_cupon(dni):    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    driver = "C:\\Git\\fala\\buscador\\chromedriver.exe"
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    chrome_options = Options()
    driver.implicitly_wait(20) # gives an implicit wait for 20 seconds

    chrome_options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')
    chrome_options.add_argument('--headless')  # Enable headless mode

    driver = webdriver.Chrome(options=chrome_options)

    driver.get("http://interbankcupones.pe/rappi")

    driver.find_element(By.ID, "document").send_keys(dni)
    time.sleep(2)
    driver.find_element(By.ID, "terms").click()
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, "form__btn--fullwidth").click()
    try:
        cupon = driver.find_element(By.CLASS_NAME, "form__box-ticket").text
    except: cupon = "Dni no valido en cuenta sueldo"
    time.sleep(2)
    print(cupon)
    driver.quit()
    return cupon

# cupon = register_cupon("your_dni")
# print(cupon)
