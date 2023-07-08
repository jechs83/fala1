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

   


def register_cupon(dni):   
    
    
    
    
     
    options = Options()
    options.add_argument('--headless')
    webdriver_path = "C:\\Git\\fala\\buscador\\chromedriver.exe"
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    options.add_argument('--window-size=1920,1080')

    options.add_argument('--user-agent=Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36')


    driver = webdriver.Chrome(service=Service(webdriver_path), options=options)
    driver.implicitly_wait(1) # gives an implicit wait for 20 seconds




    driver.get("http://interbankcupones.pe/rappi")

    # with open("C:\\Git\\fala\\buscador\\dnis.txt", 'r') as file:
    #     lines = file.readlines()
    #     dni = random.choice(lines).strip()


    driver.find_element(By.ID, "document").send_keys(dni)
    time.sleep(0.5)
    driver.find_element(By.ID, "terms").click()
    time.sleep(0.5)
    driver.find_element(By.CLASS_NAME, "form__btn--fullwidth").click()
    
    
    
    
    try:
        cupon = driver.find_element(By.CLASS_NAME, "form__box-ticket").text
        print(dni)
        print(cupon)
        #file_path = f"C:\\Git\\fala\\buscador\\dnis_valido.txt"
        #with open(file_path, 'w') as cupon_file:
         #   cupon_file.write(dni + "\n")
            #cupon_file.close()
    except:
        
        driver.quit()
        return False
        #cupon = "Dni no valido en cuenta sueldo"
        
    
  
   
 
        
    #if cupon == "Dni no valido en cuenta sueldo":
     #       return False
           
            
        

    
    #try:
     #   error = driver.find_element(By.C)

    #return cupon

# cupon = register_cupon("your_dni")
# print(cupon)

file_path = "C:\\Git\\fala\\buscador\\dnis.txt"  # Replace with the actual file path

# Read the lines from the file
with open(file_path, 'r') as file:
    lines = file.readlines()

# Remove newline characters and create an array
array = [line.strip() for line in lines]

# Print the array
print(array)

for idx, v in enumerate (array):
    
    register_cupon(v)
    if register_cupon(v)== False:
        continue

    file_path = "C:\\Git\\fala\\buscador\\dnis_valido.txt"
    with open(file_path, 'a') as cupon_file:
        cupon_file.write(v + "\n")