import sys
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime
import os
import json
import random
from datetime import date
import time
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from decouple import config

current_time= time.strftime("%H:%M")
date = date.today()
current_day= date.strftime("%d/%m/%Y")


web_url = random.choice(config("PROXY"))
client = MongoClient(config("MONGO_DB"))


from requests_html import HTMLSession
web = "https://www.metro.pe/buscapagina?sl=19ccd66b-b568-43cb-a106-b52f9796f5cd&PS=18&cc=18&sm=0&PageNumber=1&&fq=C%3a%2f1000144%2f1000098%2f"

s = HTMLSession()
r= s.get(web)

r.html.render(sleep=5)

print(r.status_code)


product = r.html.xpath("//div[@id='gallery-layout-container']", first = True)

print(product)




# def scrap (web):
#     driver = webdriver.PhantomJS()
#     options = webdriver.ChromeOptions()
#     options.add_argument('--ignore-certificate-errors')
#     #options.add_argument('--incognito')
#     #options.add_argument('--headless')
#     #driver = webdriver.Chrome(executable_path=r"/Users/javier/GIT/Sparxworks/chromedriver", options = options)
  

#     wait = WebDriverWait(driver, 30)

#     driver.get(web)

#     innerHTML = driver.execute_script("return document.body.innerHTML")

#     print(innerHTML)
  
#     # wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, ".swal2-confirm"))).click()
#     # print("se hizo click satsfactoraimente")

   

#     # products = driver.find_elements(By.XPATH,"//section[@class='vtex-product-summary-2-x-container vtex-product-summary-2-x-containerNormal overflow-hidden br3 h-100 w-100 flex flex-column justify-between center tc']")
#     # # count = len(products)
#     # print(products)
#     # count = 0
#     # for product in products:
#     #     count = count+1
#     #     if count == 8:
#     #         print("ses escrollea")
#     #         driver.execute_script("window.scrollTo(0, 300)") 
#     #         time.sleep(10)
#     #     print(count)
#     #     print()
#     #     print(product.text)

#     #     # print(product.get_attribute("href"))

#     # time.sleep(10)

# scrap(web)
# #     for i in range (122):
# #         driver.get(web+str(i+1))

# #         print(web+str(i+1))
  
# #         page_source = driver.page_source

# #         # if i <=121:
# #         #  print(page_source)

    
# #         soup = BeautifulSoup(page_source,"html.parser")
# #         #elements = soup.find("div",class_="ShowcaseGrid")
# #         print(soup)

# #         with open ( "/Users/javier/GIT/fala/wong/source.txt", "w") as f:
# #             f.write(str(soup))
# # scrap(web)

# # #         elements = soup.find("div", class_="flex flex-column min-vh-100 w-100")
# # #         elements = elements.find("script" ,type="application/ld+json").text

        





# # def scrap (web):

# #     proxies = {"http":"http://"+web_url }
        
#     res=requests.get(web,  proxies= proxies)
#     print("Respuesta del servidor :"+str(res.status_code))

   
#     res=requests.get(web,  proxies= proxies)
#     soup = BeautifulSoup(res.text, "html.parser")
#     #print(soup.prettify())
#     try:
#      elements = soup.find("div", class_="flex flex-column min-vh-100 w-100")
#      elements = elements.find("script" ,type="application/ld+json").text
#     except:
#         return False

#     elements = json.loads(str(elements))
    
#     for i in range (20):
        
#         link = elements['itemListElement'][i]["item"]["@id"] 
#         product = elements['itemListElement'][i]["item"]["name"] 
#         brand = elements['itemListElement'][i]["item"]["brand"]["name"]
#         image = elements['itemListElement'][i]["item"]["image"]
#         sku = elements['itemListElement'][i]["item"]["sku"]
#         best_price = elements['itemListElement'][i]["item"]["offers"]["lowPrice"]
#         list_price = elements['itemListElement'][i]["item"]["offers"]
#         card_price = elements['itemListElement'][i]["item"]["offers"]["offers"][0]["price"]

#         # dsct = (best_price*100/list_price)
#         # dsct = round(dsct)
      

#         print(product)
#         print(link)
#         print(brand)
#         print(image)
#         print(sku)
#         print(best_price)
#         print(list_price)
#         # print(dsct)
#         print("precio "+ str(card_price))


# scrap(web)

# #     for i in elements:
        
# #         sku = i.find("div",class_="product-item").attrs.get("data-sku")
# #         brand = i.find("div",class_="product-item").attrs.get("data-brand")
# #         category = i.find("div",class_="product-item").attrs.get("data-category")
# #         product = i.find("div",class_="product-item").attrs.get("data-name")
# #         list_price = i.find("div",class_="product-item").attrs.get("data-price")
# #         list_price = list_price.split()[1].replace(",","")
# #         try:
# #             best_price = i.find("span", class_="product-prices__value--best-price").text
# #             best_price = best_price.split()[1].replace(",","")
# #         except:best_price = 0
# #         link = i.find("div",class_="product-item").attrs.get("data-uri")
# #         img = i.find("img").attrs.get("src")
# #         market= "wong"
# #         try:
# #             dsct = i.find("div", class_= "flag discount-percent").text
# #             dsct= dsct.replace(",",".").replace("%","")
# #         except: dsct = 0

# #         print()
# #         print(product)
# #         print(url) 
# #         print(best_price) 
# #         print(sku) 
# #         print(brand)
# #         print(dsct)
# #         print(category)
# #         print(list_price) 
# #         print(link) 
# #         print(img)
# #         print()

# #         db = client["cencosud"]
# #         collection = db["market"]
# #         db2 = client["scrap"]
# #         collection2 = db2["scrap"]
# #         market = "wong"
        

# #         y = collection.find_one({"_id":market+str(sku)})
# #         z = collection2.find_one({"_id":market+str(sku)})

# #         if y :
            
# #             filter = {"_id":market+str(sku), }
# #             newvalues = { "$set":{ 
# #             "_id":market+str(sku),   
# #             "sku":str(sku), 
# #             "brand":brand,
# #             "product": product,
# #             "category":category,
# #             "list_price":float(list_price),
# #             "best_price":float(best_price),
# #             "card_price": 0,
# #             "web_dsct":float(dsct),
# #             "link": link,
# #             "image": img,
# #             "image2": "=IMAGE("+'"'+img+'"'+")",
# #             "date":current_day,
# #             "market":market,
# #             "time":current_time
# #             }}
# #             collection.update_one(filter,newvalues)
               
# #         else:
# #             print("ADICIONA NUEVO REGISTRO A BD ")
            
            
# #             data =  {
# #             "_id":market+str(sku),   
# #             "sku":str(sku), 
# #             "brand":brand,
# #             "product": product,
# #             "category":category,
# #             "list_price":float(list_price),
# #             "best_price":float(best_price),
# #             "card_price": 0,
# #             "web_dsct":float(dsct),
# #             "link": link,
# #             "image": img,
# #             "image2": "=IMAGE("+'"'+img+'"'+")",
# #             "date":current_day,
# #             "market":market,
# #             "time":current_time
            
# #             }

# #             collection.insert_one(data)
            
       
# #         y = collection2.find_one({"_id":market+str(sku)})

# #         if z :
            
# #             filter = {"_id":market+str(sku), }
# #             newvalues = { "$set":{ 
# #             "_id":market+str(sku),   
# #             "sku":str(sku), 
# #             "brand":brand,
# #             "product": product,
# #             "category":category,
# #             "list_price":float(list_price),
# #             "best_price":float(best_price),
# #             "card_price": 0,
# #             "web_dsct":float(dsct),
# #             "link": link,
# #             "image": img,
# #             "image2": "=IMAGE("+'"'+img+'"'+")",
# #             "date":current_day,
# #             "market":market,
# #             "time":current_time
# #             }}
# #             collection2.update_one(filter,newvalues)
               
# #         else:
# #             print("ADICIONA NUEVO REGISTRO A BD ")
            
            
# #             data =  {
# #             "_id":market+str(sku),   
# #             "sku":str(sku), 
# #             "brand":brand,
# #             "product": product,
# #             "category":category,
# #             "list_price":float(list_price),
# #             "best_price":float(best_price),
# #             "card_price": 0,
# #             "web_dsct":float(dsct),
# #             "link": link,
# #             "image": img,
# #             "image2": "=IMAGE("+'"'+img+'"'+")",
# #              "date":current_day,
# #             "market":market,
# #             "time":current_time
# #             }

# #             collection2.insert_one(data)
            
        

# # def scrap_category(category_url, category_on_bd):
# #     for i in range(50):
# #         success = scrap(category_url+str(i+1), category_on_bd)
# #         if success == False:
# #             return

# # path = "C:\\Git\\fala\\wong\\text\\url.txt" #  WINDOWS
# # #th = "wong//text//url.txt" # MAC OR LINUX


# # web = open(path_wong,"r").readlines()
# # links = []
# # for url in web:
# #     link = url.strip().split()
# #     links.append(link)

# # webs = []
# # for i,v in enumerate(links):
# #     for e in range (50):
# #      a=links[i][0]+str(e+1)+links[i][1]
# #      webs.append(a)

# # def wong ():
# #     for id, val  in enumerate (webs):
        
# #         scrapping = scrap(val)
# #         if scrapping == False:
# #                 continue
    

# #     auto_telegram()

# # wong()