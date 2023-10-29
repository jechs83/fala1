import sys
import time
from pymongo import MongoClient
import sys
import requests
from bs4 import BeautifulSoup
import re
from bd_record import save_data_to_mongo_db
import time
import random
from decouple import config
from datetime import datetime
from datetime import date
from decouple import config
from selenium.webdriver.common.keys import Keys

import os

from selenium import webdriver
from selenium.webdriver.common.by  import By 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

bd_name_store = "shopstar"
collection = "scrap"

def load_datetime():
    today = date.today()
    now = datetime.now()
    date_now = today.strftime("%d/%m/%Y")  
    time_now = now.strftime("%H:%M:%S")
    return date_now, time_now

webs = [
        "https://shopstar.pe/tecnologia/televisores?order=OrderByReleaseDateDESC&page=",
        "https://shopstar.pe/tecnologia/computo/laptops?order=OrderByReleaseDateDESC&page=",
        "https://shopstar.pe/tecnologia/computo/laptops/laptops-gamer?order=OrderByReleaseDateDESC&page=",
        "https://shopstar.pe/tecnologia/computo/tablets?order=OrderByReleaseDateDESC&page=",
        "https://shopstar.pe/tecnologia/computo/laptops/macbooks?order=OrderByReleaseDateDESC&page=",
        "https://shopstar.pe/tecnologia/videojuegos/consolas?order=OrderByReleaseDateDESC&page=",
        "https://shopstar.pe/tecnologia/videojuegos/nintendo?order=OrderByReleaseDateDESC&page=",
        "https://shopstar.pe/tecnologia/videojuegos/juegos-ps4?order=OrderByReleaseDateDESC&page=",
        "https://shopstar.pe/tecnologia/telefonia/celulares?order=OrderByReleaseDateDESC&page=",
        "https://shopstar.pe/tecnologia/audio/audifonos?page=",
        "https://shopstar.pe/tecnologia/audio/soundbar-y-home-theater?page=",
        "https://shopstar.pe/tecnologia/audio/audio-y-video?order=OrderByReleaseDateDESC&page=",
        "https://shopstar.pe/tecnologia/audio/parlantes?order=OrderByReleaseDateDESC&page=",
        "https://shopstar.pe/tecnologia/audio/equipos-y-torres-de-sonido?order=OrderByReleaseDateDESC&page=",
]

def shop(driver, web):
    try:
        # Open the website
        driver.get(web)
        time.sleep(4)
        max_wait_time = 10  # You can change this value

        # Scroll down the page
        scroll_distance = 1000  # Adjust as needed
        scroll_count = 5  # Change this value to scroll more or less

        for _ in range(scroll_count):
            time.sleep(0.3)
            driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
        
        html =  driver.page_source
    except KeyboardInterrupt:
        # If you manually cut or interrupt the code using Ctrl+C (KeyboardInterrupt),
        # ensure that the driver is still quit properly.
        driver.quit()

    soup = BeautifulSoup(html, 'html.parser')

    # Find the specific element by its class
    elements = soup.find_all("div", class_="vtex-search-result-3-x-galleryItem")
    if elements is None:
        return True
       
    count = 0

    for i, v in enumerate(elements):
        count = count + 1
        print("producto numero " + str(count))
        
        link = v.find("a").get('href')
        link = "https://shopstar.pe" + link
        image = v.find("img").get('src')
        product = v.find("img").get('alt')
        if product is None:
            return True
        try:
            web_dsct = v.find('span', class_='mercury-interbank-components-0-x-summary_percentualDiscount')
            web_dsct = web_dsct.text
            web_dsct = web_dsct.replace("-", "").replace("%", "")
            web_dsct = float(web_dsct)
        except:
            web_dsct = 0

        try:
            best_price = v.find("div", class_="mercury-interbank-components-0-x-summary_priceContainer")
            best_price = best_price.text
            best_price = best_price.split()
            best_price = float(best_price[1].replace(",", ""))
        except:
            best_price = 0

        try:
            list_price = v.find("span", class_="mercury-interbank-components-0-x-listPriceValue strike")
            list_price = list_price.text
            list_price = list_price.split()
            list_price = float(list_price[1].replace(",", ""))
        except:
            list_price = 0

        brand = v.find("div", class_="vtex-product-summary-2-x-productBrandContainer")
        brand = brand.text
        sku = str(load_datetime()[0]) + product
        market = "shopstar"
        card_price = 0
        card_dsct = 0
        web = "shopstar.pe"

        print(link)
        print(image)
        print(product)
        print(web_dsct)
        print(best_price)
        print(list_price)
        print(brand)

        save_data_to_mongo_db(bd_name_store, collection, market, sku, brand, product, list_price,
                        best_price, card_price, link, image, web_dsct, card_dsct, load_datetime()[0], load_datetime()[1], web)

# Create the webdriver instance outside the loop
chrome_driver_path = 'shopstar/chromedriver'  # Replace with the actual path to your chromedriver executable
options = Options()     
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# options.add_argument('--no-sandbox')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36")
options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'  # Replace with the path to your Chrome binary
service = Service(executable_path=chrome_driver_path)
service.log_path = "chromedriver.log"
driver = webdriver.Chrome(service=service, options=options)

for web in webs:
    for i in range(50):
        scrap = shop(driver, web + str(i + 1))
        if scrap is True:
            break

# Don't forget to quit the driver when done
driver.quit()
