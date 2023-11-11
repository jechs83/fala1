import time
from playwright.sync_api import sync_playwright
from bd_record import save_data_to_mongo_db
import gc
import pymongo
import sys
from decouple import config
from urls_list import *
import itertools

client = pymongo.MongoClient(config("MONGO_DB"))
db = client["brand_allowed"]
collecion = db["todo"]

bd_name_store = "wong"
collection = "scrap"

pagination = "?page="

def load_datetime():
    today = time.strftime("%d/%m/%Y")
    now = time.strftime("%H:%M:%S")
    return today, now

webs = [
            "https://www.wong.pe/tecnologia"
        
        ]




    # Add other URLs here
def allowed():
    lista_allowed = collecion.find({})

    list_allowed = [doc["brand"] for doc in lista_allowed]

    return list_allowed

list_all = allowed()

def shop(page, web):
    page.goto(web)
    page.wait_for_timeout(6000)

    scroll_distance = 2000
    scroll_count = 4
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
        link = "https://www.wong.pe"+link
        #image = element.query_selector(".vtex-product-summary-2-x-imageWrapper").get_attribute("src")
        image = element.query_selector_all("img")

        images_array = []
        for i in image:
            url_image = i.get_attribute("src")
            images_array.append(url_image)
            
        # print()  
        # print(images_array)
        # print(len(images_array))
        print("este es el producto " + str(count1))

        if len(images_array)==3:
                image = images_array[0]
        if len(images_array) == 5:
                image = images_array[2]
        if len(images_array) == 4:
                image = images_array[1]
   

        product = element.query_selector(".vtex-product-summary-2-x-nameContainer")
        product = product.inner_text()
        brand_list = product.split()
       

        for marca in brand_list:
          
            if marca.lower() in list_all:
                print(marca)
                brand = marca.lower() # Asignar la palabra común a la variable c
                break
        if marca.lower() not in list_all:
                continue
        brand = marca

        best_price = element.query_selector(".wongio-store-theme-7-x-containerPriceListPLP")
       
        list_price= element.query_selector(".wongio-store-theme-7-x-promo-price-ref")
        
        try:
            list_price = list_price.inner_text()
            list_price = list_price.split()
            list_price = float(list_price[3].replace(",",""))
        except: list_price = 0

        try:
            best_price = best_price.inner_text()
            best_price = best_price.split()
            best_price = float(best_price[3].replace(",",""))
        except:
            best_price = 0

        web_dsct = element.query_selector(".vtex-flex-layout-0-x-flexRow")
        try:
            web_dsct = web_dsct.inner_text()
            web_dsct = int(web_dsct.replace("-","").replace("%",""))
        except: web_dsct = 0

        # sku = product+load_datetime()[0]
        sku = f"{load_datetime()[0]}{product}"
        print("###############################")
        print(web_dsct)
        print(list_price)
        print(best_price)
        print(brand)
        print(product)
        print(link)
        print(image)
        print(web)
        print()
        


        market = "wong"
        card_dsct = 0

        card_price = 0

        if brand == "None"                                                                                                                               == "None":
            continue
        try:
            save_data_to_mongo_db(bd_name_store, collection, market, sku, brand, product, list_price,
                        best_price, card_price, link, image, web_dsct, card_dsct, load_datetime()[0], load_datetime()[1], web)
        except:
            print("data base offline")
        
        gc.collect()
        #Save data to MongoDB here


# with sync_playwright() as p:
#     browser = p.chromium.launch()
#     page = browser.new_page()

#     while True:
#         for i, web in enumerate (webs):
#             for i in range(50):
                
#                 scrap = shop(page, web+pagination + str(i + 1))
#                 if scrap == False:
#                     break
                
#         browser.close()
#         time.sleep(5)  # Wait for 30 minutes before running the loop again

argument = sys.argv[1]
print("este es el argument "+argument)
if argument == "1":
    web_wong = list1
elif argument == "2":
    web_wong = list2
elif argument == "3":
    web_wong = list3
elif argument == "4":
    web_wong = list4

else:
    print("Invalid argument. Use '1' to '4'.")



with sync_playwright() as p:
    browser = p.chromium.launch(timeout=30000)  # Set a longer timeout for browser launch
    page = browser.new_page()  

    web_shop_cycle = itertools.cycle(web_wong)


    try:
        while True:
            for i, web in enumerate(web_shop_cycle):
                for i in range(50):
                    scrap = shop(page, web + pagination + str(i + 1))
                    if scrap == False:
                        break
    except KeyboardInterrupt:
        print("Script interrupted. Closing the browser gracefully...")
    finally:
        page.close()

    time.sleep(5)  # Wait for 5 seconds before exiting





       
