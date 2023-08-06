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
          time.sleep(2)


    
          for i in range (2):
            driver.execute_script("window.scrollBy(0, 1500);")
            time.sleep(0.5)  # Wait for a short while after each scroll
    
          time.sleep(1)
          source_html = driver.page_source



          # Assuming you have already defined the 'convert_to_float' function
          # ...

          # Replace 'YOUR_URL_HERE' with the actual URL from which you want to extract data
   
          # response = requests.get(url)
          # soup = BeautifulSoup(response.content, 'html.parser')\
          
          soup = BeautifulSoup(source_html, 'html.parser')

     

          elements = soup.find_all("div", class_="vtex-search-result-3-x-galleryItem vtex-search-result-3-x-galleryItem--normal vtex-search-result-3-x-galleryItem--grid pa4")

          for element in elements:


               link = element.find("a")['href']
               link = "https://shopstar.pe"+link
               image = element.find("img")['src']
               market = "shopstar"

               product = element.find('h3', class_='vtex-product-summary-2-x-productNameContainer')
               product = product.text.strip()
             
                

              

               brand = element.find("span", class_="vtex-product-summary-2-x-productBrandName")
               brand = brand.text.strip()  if brand else "sin marca"

               sku = product + str(current_date)
               try:
                    card_price = element.find("span", class_="mercury-interbank-components-0-x-summary_priceInterbankContainer").text
                    card_price =re.sub(r'[^\d.]', '', card_price)
                    card_price = card_price.replace(",", "")
                    card_price = card_price.replace("S/ ", "")
               except:card_price = 0
             
               try:
                    list_price = element.find("span", class_="mercury-interbank-components-0-x-listPrice").text
                    list_price=re.sub(r'[^\d.]', '', list_price)
                    list_price = list_price.replace(",", "").replace("S/ ", "")
               except:list_price = 0

               try:
                    best_price = element.find("span", class_="mercury-interbank-components-0-x-sellingPriceValue").text
                    best_price =re.sub(r'[^\d.]', '', best_price)
                    best_price = best_price.replace(",", "").replace("S/ ", "")
               except: best_price = 0

               try:
                    dsct = element.find("span", class_="mercury-interbank-components-0-x-summary_percentualDiscount").text
                    dsct = dsct.replace("-","").replace("%","")
                    
               except: dsct = 0

               card_dsct = dsct
              

          # Here you can save the extracted data to a file or any other desired storage
          # ...


                    
               print("marca "+brand)
               print("modelo "+product)
               print("tarjeta "+str(card_price))
               print("lista "+str(list_price))
               print("online "+str(best_price))
               print("descuento "+str(dsct))
               print(link)
               print(image)
               print()
              

               db = client["scrap"]
               collection = db["scrap"]

               # Define the data dictionary
               data = {
               "_id": market + sku,
               "sku": sku,
               "market": market,
               "brand": str(brand),
               "product": str(product),
               "list_price": float(list_price),
               "best_price": float(best_price),
               "card_price": float(card_price),
               "web_dsct": float(dsct),
               "card_dsct": float(card_dsct),
               "link": str(link),
               "image": str(image),
               "date": current_date,
               "time": current_time,
               "home_list": web
               }

               # Use update_one with upsert=True to insert or update the data
               collection.update_one({"_id": data["_id"]}, {"$set": data}, upsert=True)
               print("se grabo")

            #    if  product: 
            #        return True
            #    else: 
            #     continue

# source_html = scrap(web)
# with open ("source.html", "w+") as f:
#         f.write(source_html)


def initialize_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    # Provide the path to the chromedriver executable
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
    driver.implicitly_wait(20) # gives an implicit wait for 20 seconds
    return driver


if __name__ == "__main__":
    # urls = ["https://shopstar.pe/tecnologia/computo?order=OrderByReleaseDateDESC&page=",
    #        "https://shopstar.pe/tecnologia/televisores?order=OrderByReleaseDateDESC&page="
    #        ]

    numero = int(sys.argv[1])

    if numero == 1:
      urls = urls_list.list1
    if numero == 2:
      urls = urls_list.list2
    websites = []
    for i,v in enumerate  (urls) :
        for e in range(200):
            websites.append(v+str(e+1))
    grouped_arrays = [websites[i:i + len(urls)] for i in range(0, len(websites), len(urls))]

    # print(grouped_arrays)
      
    count = 0
    driver = initialize_driver()
    for webs in grouped_arrays:
       
        for web  in webs:
            scrapping = scrap(driver,web)
            print(web)
            count= count+1
            print(count)
            print(scrapping)
            # if scrapping == None:
            #     continue

    

    driver.quit()


