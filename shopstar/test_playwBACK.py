import time
import random
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from bd_record import save_data_to_mongo_db



bd_name_store = "shopstar"
collection = "scrap"

def load_datetime():
    today = time.strftime("%d/%m/%Y")
    now = time.strftime("%H:%M:%S")
    return today, now

webs = [
    
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
        "https://shopstar.pe/tecnologia/televisores?order=OrderByReleaseDateDESC&page=",
    # Add other URLs here
]

def shop(page, web):
    page.goto(web)
    page.wait_for_timeout(4000)

    scroll_distance = 1000
    scroll_count = 5
    for _ in range(scroll_count):
        page.evaluate(f"window.scrollBy(0, {scroll_distance});")
        page.wait_for_timeout(300)

    elements = page.query_selector_all(".vtex-search-result-3-x-galleryItem")


    if not elements:

        return True

    count = 0

    for element in elements:

        # inner_html = element.evaluate('(element) => element.innerHTML')
    
        # # Print the inner HTML
        # # Use the evaluate function to get the inner HTML of the element
        # inner_html = element.evaluate('(element) => element.innerHTML')
        
        # # Parse the inner HTML using BeautifulSoup
        # soup = BeautifulSoup(inner_html, 'html.parser')

        # # Prettify the HTML content
        # prettified_html = soup.prettify()
        
        # # Print the prettified HTML
        # print("Prettified HTML of the element:")
        # print(prettified_html)
        # count += 1
        # print(f"Producto numero {count}")

        link = element.query_selector("a").get_attribute("href")
        link = "https://shopstar.pe" + link

        image = element.query_selector("img").get_attribute("src")

        #product = element.query_selector("img").get_attribute("alt")


        product_items = element.query_selector_all(".mercury-interbank-components-0-x-currencyContainer")


        product_items = [element.inner_text() for element in elements]

        for price_text in product_items:
     
            
            element = price_text.split('\n')
    
            if len(element) == 7:
                web_dsct = element[2]
                web_dsct = web_dsct.replace("-","").replace("%","")
                try:
                    web_dsct = int(web_dsct)
                except: web_dsct = "None"

                if web_dsct == "None":
                    brand = element[1]
                    product = element[2]
                    web_dsct = element[3]
                    web_dsct = web_dsct.replace("-","").replace("%","")
                    web_dsct = int(web_dsct)
                
                    list_price = element[4]
                    list_price = float(list_price.replace("S/","").replace(",",""))

                    best_price = element[5]
                    best_price = float(best_price.replace("S/","").replace(",",""))
                    card_price = 0
             
                else:
                    brand = element[0]
                    product = element[1]
                    card_price = element[3]
                    list_price = element[4]
                    best_price = element[5]
   
#############################################################
            if len(element) == 6:

                brand = element[0]
                product = element[1]
                web_dsct = element[2]
                web_dsct = int(web_dsct.replace("-","").replace("%",""))

                list_price = element[3]
                list_price = float(list_price.replace("S/","").replace(",",""))
                best_price = element[4]
                best_price = float(best_price.replace("S/","").replace(",",""))
                card_price = 0

            if len(element) == 4:
                brand = element[0]
                product = element[1]
                web_dsct = 0
                card_price = 0
                list_price = 0
                best_price = element[2]
                best_price = float(best_price.replace("S/","").replace(",",""))

               
                    
        sku = f"{load_datetime()[0]}{product}"

       
        market = "shopstar"
        card_price = 0
        card_dsct = 0
        web = web
        print()
        print(link)
        print(image)
        print(product)
        print(web_dsct)
        print(best_price)
        print(list_price)
        print(brand)
        save_data_to_mongo_db(bd_name_store, collection, market, sku, brand, product, list_price,
                        best_price, card_price, link, image, web_dsct, card_dsct, load_datetime()[0], load_datetime()[1], web)

        # Save data to MongoDB here

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    while True:
        for web in webs:
            for i in range(50):
                scrap = shop(page, web + str(i + 1))
                if scrap:
                    break
        browser.close()
        time.sleep(30)  # Wait for 30 minutes before running the loop again

       
