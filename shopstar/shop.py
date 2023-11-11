import time
import random
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pymongo
from bd_record import save_data_to_mongo_db
import gc
from urls_list import *
import sys
import itertools

from decouple import config
client = pymongo.MongoClient(config("MONGO_DB"))
db = client["brand_allowed"]
collecion = db["todo"]


bd_name_store = "shopstar"
collection = "scrap"

def load_datetime():
    today = time.strftime("%d/%m/%Y")
    now = time.strftime("%H:%M:%S")
    return today, now


def allowed():
    lista_allowed = collecion.find({})

    list_allowed = [doc["brand"] for doc in lista_allowed]

    return list_allowed


list_all = allowed()

webs = [
        ("https://shopstar.pe/tecnologia/televisores?initialMap=c,c&initialQuery=tecnologia/televisores&map=category-1,category-2&order=OrderByReleaseDateDESC&page=", "&priceRange=14%20TO%203022")

#         "https://shopstar.pe/electrohogar/lavado?order=OrderByReleaseDateDESC&page=",
# "https://shopstar.pe/electrohogar/cocina?order=OrderByReleaseDateDESC&page=",
# "https://shopstar.pe/electrohogar/refrigeracion?order=OrderByReleaseDateDESC&page=",
# "https://shopstar.pe/electrohogar/climatizacion?order=OrderByReleaseDateDESC&page=",
# "https://shopstar.pe/electrohogar/electrodomesticos/aspirado?order=OrderByReleaseDateDESC&page=",
]
    # Add other URLs here

def shop(page, web):
    # try:

        page.goto(web, timeout=12000) 
        page.wait_for_timeout(6000)

        scroll_distance = 1500
        scroll_count = 3
        for _ in range(scroll_count):
            page.evaluate(f"window.scrollBy(0, {scroll_distance});")
            page.wait_for_timeout(400)

        elements = page.query_selector_all(".vtex-search-result-3-x-galleryItem")
        if not elements:
            return False
        count1 = 0
        for element in elements:
            count1 = count1+1

            link = element.query_selector("a").get_attribute("href")
            link = "https://shopstar.pe" + link

            image = element.query_selector("img").get_attribute("src")

            product = element.query_selector("img").get_attribute("alt")
            try:
                brand = element.query_selector(".vtex-product-summary-2-x-productBrandName")
                brand = brand.inner_text()
            except:
                brand = element.query_selector(".vtex-product-summary-2-x-productBrandContainer")
                brand = brand.inner_text()

            if not brand:
                continue

            if brand.lower() not in list_all:
                continue

            interbank_price = element.query_selector(".mercury-interbank-components-0-x-summary_priceContainer")

            try:
                interbank_price = interbank_price.inner_text()
                interbank_price = interbank_price.split()
                interbank_price = float(interbank_price[1].replace(",",""))
                best_price = interbank_price
            
            except: best_price = 0

            #list_prices = element.query_selector(".mercury-interbank-components-0-x-summary_normalPricesContainer")
            list_prices = element.query_selector(".mercury-interbank-components-0-x-summary_pricesContainer")
            
            
            list_prices = list_prices.inner_text()
            list_prices = list_prices.split()
            arr_y = list_prices
            
            if list_prices == []:
                list_price=0
        

            if len(list_prices)==9:
                list_price = float(list_prices[4].replace(",",""))
                best_price = float(list_prices[6].replace(",",""))
                card_price = float(list_prices[6].replace(",",""))
                web_dsct =  int(list_prices[0].replace("-","").replace("%",""))

            if len(list_prices)==7:
                list_price = float(list_prices[4].replace(",",""))
                best_price = float(list_prices[6].replace(",",""))
                card_price = float(list_prices[2].replace(",",""))
                web_dsct =  int(list_prices[0].replace("-","").replace("%",""))

            if len(list_prices)==6:
                list_price = float(list_prices[5].replace(",",""))
                best_price = float(list_prices[3].replace(",",""))
                card_price = float(list_prices[1].replace(",",""))
                web_dsct = 0

            if len(list_prices)==4:
                best_price = float(list_prices[3].replace(",",""))
                card_price = float(list_prices[1].replace(",",""))
                web_dsct = 0
                list_price = 0

            

            print("######### "+str(len(list_prices)))  
            print(arr_y)
            print(web) 
            print(brand)
            print(list_price)
            print(best_price)
            print(card_price)
            print(link)
            print(image)
            print(product)
            print(web_dsct)
            print(web)
            print("############################################")
            print("producto numero "+str(count1))
            print()


            market = "shopstar"
            sku = f"{load_datetime()[0]}{product}"
            card_dsct = 0
            try:
                save_data_to_mongo_db(bd_name_store, collection, market, sku, brand, product, list_price,
                            best_price, card_price, link, image, web_dsct, card_dsct, load_datetime()[0], load_datetime()[1], web)
            except:
                print("data base offline")
            
    #         # Save data to MongoDB here
    # except Exception as e:
    #     print(f"Error during scraping: {e}")
    #     # Handle the error or log it as needed


argument = sys.argv[1]
print("este es el argument "+argument)
if argument == "1":
    web_shop = list1
elif argument == "2":
    web_shop = list2
elif argument == "3":
    web_shop = list3
elif argument == "4":
    web_shop = list4


else:
    print("Invalid argument. Use '1' to '4'.")



with sync_playwright() as p:
    #browser = p.chromium.launch(headless=False)
    browser = p.chromium.launch(timeout=30000)  # Set a longer timeout for browser launch
    page = browser.new_page(timeout=30000)  

    # Create an iterator that cycles through the web shop URLs indefinitely
    web_shop_cycle = itertools.cycle(web_shop)

    while True:
        for _ in range(50):
            web = next(web_shop_cycle)
            for i in range(50):
                # if i <=46:
                #   continue
                scrap = shop(page, web + "?page=" + str(i + 1))
                if scrap == False:
                    break

        page.close()
        time.sleep(5)
       

