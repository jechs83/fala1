import time
import random
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from bd_record import save_data_to_mongo_db
import gc



bd_name_store = "shopstar"
collection = "scrap"

def load_datetime():
    today = time.strftime("%d/%m/%Y")
    now = time.strftime("%H:%M:%S")
    return today, now

webs = [
    
    "https://shopstar.pe/tecnologia/televisores?order=OrderByReleaseDateDESC&page=",
        "https://shopstar.pe/tecnologia/computo/laptops?order=OrderByReleaseDateDESC&page=",
        "https://shopstar.pe/tecnologia/computo/laptops/laptops-gamer?order=OrderByReleaseDateDESC&page=",
        "https://shopstar.pe/tecnologia/computo/tablets?order=OrderByReleaseDateDESC&page=",
        "https://shopstar.pe/tecnologia/computo/laptops/macbooks?order=OrderByReleaseDateDESC&page=",
    # Add other URLs here
]

def shop(page, web):
    page.goto(web)
    page.wait_for_timeout(6000)

    scroll_distance = 1000
    scroll_count = 5
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

        try:
            percentual_discount_element = page.query_selector('.mercury-interbank-components-0-x-summary_percentualDiscount')
            text = percentual_discount_element.inner_text()
            web_dsct = int(text.replace("%","").replace("-",""))
        except:
            web_dsct = 0
    

        currency_containers = element.query_selector_all('.mercury-interbank-components-0-x-currencyContainer')
        count = 0

        # Iterate through the elements and extract their text
        for currency_container in currency_containers:
            count = count+1
            if count == 2:
                continue
       
            price_list = [currency_container.inner_text() for currency_container in currency_containers]

            if len(price_list) == 2:
                print(len(price_list))
                list_price = float(price_list[0].replace("S/","").replace(",",""))
                best_price = float(price_list[1].replace("S/","").replace(",",""))
                card_price = 0
            if len(price_list) == 3:
                print(len(price_list))
                list_price = float(price_list[1].replace("S/","").replace(",",""))
                best_price = float(price_list[2].replace("S/","").replace(",",""))
                card_price = float(price_list[0].replace("S/","").replace(",",""))

            if len(price_list) == 1:
                print(len(price_list))

                list_price = float(price_list[0].replace("S/","").replace(",",""))
                card_price = 0
                best_price = 0


            # Print the list of text values
            
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
            # Save data to MongoDB here


with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    while True:
        for web in webs:
            for i in range(50):
             
                    scrap = shop(page, web + str(i + 1))
                    if scrap == False:
                        break
               
        browser.close()
        time.sleep(5)  # Wait for 30 minutes before running the loop again
       

