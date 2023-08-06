from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by  import By 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time
from bd_record import save_data_to_mongo_db, dia
import random
from datetime import datetime
from decouple import config
from pymongo import MongoClient
client = MongoClient(config("MONGO_DB"))
chromedriver_path = "/Users/javier/GIT/fala/shopstar/chromedriver"

def dia():
    now = datetime.now()
    date = now.strftime("%d/%m/%Y")
    #date = date.today()
    time = now.strftime("%H:%M:%S")
    return date, time

def convert_to_float(value):
    try:
        return float(value.replace("S/ ", "").replace(",", "").replace("-","").replace("%",""))
    except ValueError:
        return 0



def close_popup(driver):
    try:
        popup_element = driver.find_element(By.ID,"btnNoIdWpnPush")
        popup_element.click()
        print("Popup closed successfully.")
    except:
        print("Popup not found or could not be closed.")
    try:
        popup_element2 = driver.find_element(By.CLASS_NAME,"wpn-popup-close")
        popup_element2.click()
        print("Popup2 closed successfully.")
    except:
        print("Popup2 not found or could not be closed.")


current_date = dia()[0]
current_time = dia()[1]



def scrap(driver,web):    
        # options = Options()
        # #options.add_argument('--headless')
        # options.add_argument('--window-size=1920,1080')
        # driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
        # driver.implicitly_wait(20) # gives an implicit wait for 20 seconds
  
        driver.get(web)


    
        for i in range (2):
            driver.execute_script("window.scrollBy(0, 1500);")
            time.sleep(0.3)  # Wait for a short while after each scroll

        source_html = driver.page_source

        with open ("source.html", "w+") as f:
                f.write(source_html)
        print("paso por aqui")
        
        time.sleep(20)
'''
        elements =  driver.find_elements(By.CLASS_NAME,"vtex-product-summary-2-x-container")

        for element in elements:
                
                link = element.find_element(By.CSS_SELECTOR, "a.vtex-product-summary-2-x-clearLink").get_attribute("href")
                image = element.find_element(By.CSS_SELECTOR,"img.vtex-product-summary-2-x-imageNormal.vtex-product-summary-2-x-image").get_attribute("src")
                market = "shopstar"
        
                try:
                     brand = element.find_element(By.CLASS_NAME, "vtex-product-summary-2-x-productBrandName").text
                except:
                     brand = None
            
                try:
                     product = element.find_element(By.CLASS_NAME, "vtex-product-summary-2-x-productBrand").text
                except:
                     product = None
                    
                sku = product+str(current_date)
                try:
                     card_price = element.find_element(By.CLASS_NAME, "mercury-interbank-components-0-x-summary_priceContainer").text
                     card_price = convert_to_float(card_price)
                except:
                     card_price = 0
                
                try:
                     list_price = element.find_element(By.CLASS_NAME, "mercury-interbank-components-0-x-listPrice").text
                     list_price = convert_to_float(list_price)
                except:
                     list_price = 0

                try:
                     best_price = element.find_element(By.CLASS_NAME, "mercury-interbank-components-0-x-sellingPriceValue").text
                     best_price = convert_to_float(best_price)
                except:
                     best_price = 0

                try:
                     dsct = element.find_element(By.CLASS_NAME, "mercury-interbank-components-0-x-summary_percentualDiscount").text
                     dsct= convert_to_float(dsct)
                except:
                     dsct = 0
                card_dsct = dsct
                    
          
                print("marca "+brand)
                print("modelo "+product)
                print("tarjeta "+str(card_price))
                print("lista "+str(list_price))
                print("online "+str(best_price))
                print("descuento "+str(dsct))
                print(link)
                print(image)
                print()
'''         

                # db = client["TEST"]
                # collection = db["test"]

                # # Define the data dictionary
                # data = {
                #     "_id": market + sku,
                #     "sku": sku,
                #     "market": market,
                #     "brand": str(brand),
                #     "product": str(product),
                #     "list_price": float(list_price),
                #     "best_price": float(best_price),
                #     "card_price": float(card_price),
                #     "web_dsct": float(dsct),
                #     "card_dsct": float(card_dsct),
                #     "link": str(link),
                #     "image": str(image),
                #     "date": current_date,
                #     "time": current_time,
                #     "home_list": web
                # }

                # # Use update_one with upsert=True to insert or update the data
                # collection.update_one({"_id": data["_id"]}, {"$set": data}, upsert=True)

# source_html = scrap(web)
# with open ("source.html", "w+") as f:
#         f.write(source_html)


def initialize_driver():
    options = Options()
    # options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    # Provide the path to the chromedriver executable
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
    driver.implicitly_wait(20) # gives an implicit wait for 20 seconds
    return driver


if __name__ == "__main__":

    websites = []
    for i in range (200):
        websites.append("https://shopstar.pe/tecnologia/televisores?order=OrderByReleaseDateDESC&page="+str(i+1))

    driver = initialize_driver()
    for web in websites:
        scrap(driver,web)
    

    driver.quit()


