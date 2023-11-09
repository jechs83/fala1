import time
import random
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from bd_record import save_data_to_mongo_db
import gc
from urls_list import *
import sys
import pymongo
from decouple import config

client = pymongo.MongoClient(config("MONGO_DB"))
db = client["brand_allowed"]
collecion = db["todo"]

bd_name_store = "coolbox"
collection = "scrap"

pagination = "?page="

def load_datetime():
    today = time.strftime("%d/%m/%Y")
    now = time.strftime("%H:%M:%S")
    return today, now

webs = ["https://www.coolbox.pe/outlet?layout=grid&order=OrderByPriceDESC",
            "https://www.coolbox.pe/tv-y-video/televisores",
                "https://www.coolbox.pe/tv-y-video/convertidores",
            "https://www.coolbox.pe/celulares-y-accesorios/celulares",
            "https://www.coolbox.pe/celulares-y-accesorios/relojes-inteligentes",
            "https://www.coolbox.pe/scooters-y-bicicletas-electricas/scooters-electricos",
        "https://www.coolbox.pe/scooters-y-bicicletas-electricas?initialMap=c&initialQuery=scooters-y-bicicletas-electricas&map=category-1,category-2,category-2&query=/scooters-y-bicicletas-electricas/bicicletas-electricas/bicicletas-mecanicas&searchState",
        "https://www.coolbox.pe/scooters-y-bicicletas-electricas/motos-electricas",
        "https://www.coolbox.pe/laptops-monitores-y-tablets/laptops/laptops-gamer",
        "https://www.coolbox.pe/gamer/accesorios-gamer",
        "https://www.coolbox.pe/computo/componentes-de-computo",
        "https://www.coolbox.pe/gamer/sillas-y-mesas-gamer",
        "https://www.coolbox.pe/videojuegos-y-gamer/consolas",
        "https://www.coolbox.pe/laptops-monitores-y-tablets/monitores",
                "https://www.coolbox.pe/audio/parlantes",
                "https://www.coolbox.pe/audio/audifonos",
                "https://www.coolbox.pe/audio/barras-y-sistemas-de-sonido"


#         "https://shopstar.pe/electrohogar/lavado?order=OrderByReleaseDateDESC&page=",
# "https://shopstar.pe/electrohogar/cocina?order=OrderByReleaseDateDESC&page=",
# "https://shopstar.pe/electrohogar/refrigeracion?order=OrderByReleaseDateDESC&page=",
# "https://shopstar.pe/electrohogar/climatizacion?order=OrderByReleaseDateDESC&page=",
# "https://shopstar.pe/electrohogar/electrodomesticos/aspirado?order=OrderByReleaseDateDESC&page=",
]
    # Add other URLs here
def allowed():
    lista_allowed = collecion.find({})

    list_allowed = [doc["brand"] for doc in lista_allowed]

    return list_allowed


list_all = allowed()





def shop(page, web):
    page.goto(web, timeout=60000) 
    page.wait_for_timeout(6000)

    scroll_distance = 1500
    scroll_count = 4
    for _ in range(scroll_count):
        page.evaluate(f"window.scrollBy(0, {scroll_distance});")
        page.wait_for_timeout(400)

    elements = page.query_selector_all(".coolboxpe-search-result-0-x-galleryItem")
    if not elements:
        return False
    count1 = 0
    for element in elements:
        count1 = count1+1

        link = element.query_selector("a").get_attribute("href")
        link = "https://www.coolbox.pe"+link
        image = element.query_selector("img").get_attribute("src")
        brand = element.query_selector(".vtex-store-components-3-x-productBrandContainer")
        brand = brand.inner_text()

        if not brand:
            break
  
        if brand.lower() not in list_all:
            continue


        product = element.query_selector(".vtex-product-summary-2-x-nameContainer")
        product = product.inner_text()

        price1 = element.query_selector(".vtex-store-components-3-x-sellingPrice")
        
        try:
            price1 = price1.inner_text()
            price1 = price1.split()
            best_price = float(price1[1].replace(",",""))
        except: best_price = 0
        
     

        price2 = element.query_selector(".vtex-store-components-3-x-listPrice")
     
        try:
            price2 = price2.inner_text()
            price2 = price2.split()
            list_price = float(price2[1].replace(",",""))
        
        except:
            list_price = 0

      

        web_dsct = element.query_selector(".vtex-store-components-3-x-discountContainer")
        try:
            web_dsct = web_dsct.inner_text()
            web_dsct = int(web_dsct.replace("-","").replace("%",""))
        except: web_dsct = 0

        # sku = product+load_datetime()[0]
        sku = f"{load_datetime()[0]}{product}"

        print(web_dsct)
        print(list_price)
        print(best_price)
        print(brand)
        print(product)
        print(link)
        print(image)
        print(sku)
        print(web)
        print()

        market = "coolbox"
        card_dsct = 0

        card_price = 0
        try:
            save_data_to_mongo_db(bd_name_store, collection, market, sku, brand, product, list_price,
                        best_price, card_price, link, image, web_dsct, card_dsct, load_datetime()[0], load_datetime()[1], web)
        except:
            print("data base offline")
        
        #Save data to MongoDB here
argument = sys.argv[1]
print("este es el argument "+argument)
if argument == "1":
    web_cool = list1
elif argument == "2":
    web_cool = list2
elif argument == "3":
    web_cool = list3
elif argument == "4":
    web_cool = list4

else:
    print("Invalid argument. Use '1' to '4'.")



# with sync_playwright() as p:
#     browser = p.chromium.launch()
#     page = browser.new_page()

#     while True:
#         for i, web in enumerate (web_cool):
#             for i in range(50):
                
#                 scrap = shop(page, web+pagination + str(i + 1))
#                 if scrap == False:
#                     break
                
#         browser.close()
#         time.sleep(5)  # Wait for 30 minutes before running the loop again

       

with sync_playwright() as p:
    while True:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        for i, web in enumerate(web_cool):
            for i in range(50):
                if web.endswith("DESC"):
                    pagination ="&page="

                scrap = shop(page, web + pagination + str(i + 1))
                if scrap == False:
                    break
        
        browser.close()
        time.sleep(1)  # Wait for 5 seconds before running the loop again
