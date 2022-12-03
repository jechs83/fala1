import sys
import requests
from urllib import request
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import datetime
from decouple import config
import random
from datetime import date
import time
import json
current_time= time.strftime("%H:%M")
date = date.today()
current_day= date.strftime("%d/%m/%Y")
from decouple import config
web_url = random.choice(config("PROXY"))
client = MongoClient(config("MONGO_DB"))

first_sku = None

web = "https://www.oechsle.pe/tecnologia"
def scrap (web):
    
    proxies = {"http":"http://"+web_url }
    res=requests.get(web,  proxies= proxies)
    print("Respuesta del servidor :"+str(res.status_code))
    soup = BeautifulSoup(res.text, "html.parser")

    product = soup.find_all("script")
    count = 0
    for i in product:
        count = count+1
        if count ==30:
           
            print("###############")
            products_id = i.text.strip()
            products_id = products_id.replace("vtex.events.addData(","").replace(");","")
  



    pro_ids = json.loads(str(products_id))

    pro_ids = pro_ids["shelfProductIds"]

    pro_ids = str(pro_ids).replace("[","").replace("]","").replace("'","")




    # for i in pro_ids:
    #     print(i)

    
    web = "https://www.oechsle.pe/api/catalog_system/pub/products/search/?fq="

    api_oh = web+pro_ids
    api_oh = api_oh.replace(" ","")
    return api_oh
   

url = scrap(web)
# print(url)

url = "https://www.oechsle.pe/api/catalog_system/pub/products/search/?fq=1886762,2075464,2221017,2202851,2202835,2096011,2086171,2075466,2075463,2059656,1956537,1951071,2221018,2166824,2156213,2119640,2114102,2075462,2044047,2033816,1000374991,1000243254,2238603,2238432,2233513,2229530,2174709,2160928,2145283,2127663,2119644,2091551,1927300,1000290146,1000283438,1000283437"
def scrap2 (url):
   
    proxies = {"http":"http://"+web_url }
        
    # res=requests.get(url,  proxies= proxies)
    # print("Respuesta del servidor :"+str(res.status_code))

    html = request.urlopen(url).read()
    soup = BeautifulSoup(html,'html.parser')
    data = soup.text
    # data - data.replace("'",'"')
    site_json=json.loads(data)

    with open("/Users/javier/GIT/fala/plazavea/html.txt", "w") as f:
        f.write(str(site_json))


    print(site_json[0])




 

scrap2(url)

# url = scrap(web)


# def w (cc):

#     proxies = {"http":"http://"+web_url }
        
#     res=requests.get(cc,  proxies= proxies)
#     print("Respuesta del servidor :"+str(res.status_code))

#     soup = BeautifulSoup(res.text, "html.parser")


#     try:
#      elements = soup.find_all("div",class_="product instock")
#     except: elements = None
       
#     count=0
    
#     for i in elements:
#         count= count+1
#         print(count)
       
#         try:
#             brand = i.attrs.get("data-brand")
#         except: brand = 0
      

#         try:
#             link = i.attrs.get("data-link")
#         except: link = None
        

        
#         sku = i.attrs.get("data-id")
       

#         print(str(sku)+" "+ str(first_sku))
#         if  sku == first_sku:
#             print("se repite SKU")
#             print(str(sku)+" "+ str(first_sku))
      
#             return False 

#         if count == 1:
#             first_sku = sku
       

#         try:
#             product = i.attrs.get("data-name")
#         except: product = None
        

#         try:
#             stock = i.attrs.get("data-stock")
#         except: stock = None
        
#         if stock == "True":
#             stock = "Si"
#         if stock == "False":
#             stock = "No"
        

#         try:
#             image = i.find("img").attrs.get("src")
#         except: image = None
       

#         try:
#             list_price = i.find("span", class_="text text-gray-light text-del fz-11 fz-lg-13 ListPrice").text
#         except: list_price = 0
#         list_price = str(list_price).replace("S/. ","").replace(",","")
        

#         try:
#             best_price = i.find("span", class_="text fz-lg-15 fw-bold BestPrice").text
#         except: best_price = 0
#         best_price = str(best_price).replace("S/. ","").replace(",","")
        


#         try:
#             dsct = i.find("span", class_="flag-of ml-10 lol").text
#         except: dsct = 0
#         dsct = str(dsct).replace("-","").replace(" %","").replace(",",".")

#         # print(brand)
#         # print(link)
#         # print(product)
#         # print(image)
#         # print(list_price)
#         # print(best_price)
#         # print(dsct)
#         # print(stock)
        
#         db = client["oh"]
#         collection = db["market2"]
#         db2 = client["scrap1"]
#         collection2 = db2["scrap1"]
#         market = "vea"
    
#         category = None
        

#         y = collection.find_one({"_id":market+str(sku)})
#         z = collection2.find_one({"_id":market+str(sku)})

#         if y :
            
#             filter = {"_id":market+str(sku), }
#             newvalues = { "$set":{ 
#             "_id":market+str(sku),   
#             "sku":str(sku), 
#             "brand":brand,
#             "product": product,
#             "category":category,
#             "list_price":float(list_price),
#             "best_price":float(best_price),
#             "card_price": 0,
#             "web_dsct":float(dsct),
#             "link": link,
#             "image": image,
#             "date":current_day,
#             "market":market,
#             "time":current_time
#             }}
#             collection.update_one(filter,newvalues)
               
#         else:
#             #print("ADICIONA NUEVO REGISTRO A BD ")
            
            
#             data =  {
#             "_id":market+str(sku),   
#             "sku":str(sku), 
#             "brand":brand,
#             "product": product,
#             "category":category,
#             "list_price":float(list_price),
#             "best_price":float(best_price),
#              "card_price": 0,
#             "web_dsct":float(dsct),
#             "link": link,
#             "image": image,
#             "date":current_day,
#             "market":market,
#             "time":current_time
            
#             }

#             collection.insert_one(data)
            
       
#         y = collection2.find_one({"_id":market+str(sku)})

#         if z :
            
#             filter = {"_id":market+str(sku), }
#             newvalues = { "$set":{ 
#             "_id":market+str(sku),   
#             "sku":str(sku), 
#             "brand":brand,
#             "product": product,
#             "category":category,
#             "list_price":float(list_price),
#             "best_price":float(best_price),
#             "card_price": 0,
#             "web_dsct":float(dsct),
#             "link": link,
#             "image": image,
#             "date":current_day,
#             "market":market,
#             "time":current_time
#             }}
#             collection2.update_one(filter,newvalues)
               
#         else:
#             #print("ADICIONA NUEVO REGISTRO A BD ")
            
            
#             data =  {
#             "_id":market+str(sku),   
#             "sku":str(sku), 
#             "brand":brand,
#             "product": product,
#             "category":category,
#             "list_price":float(list_price),
#             "best_price":float(best_price),
#             "card_price": 0,
#             "web_dsct":float(dsct),
#             "link": link,
#             "image": image,
#             "date":current_day,
#             "market":market,
#             "time":current_time
#             }

#             collection2.insert_one(data)
        
   
            

# # def scrap_category(category_url, category_on_bd):
# #     for i in range(50):
# #         success = scrap(category_url+str(i+1), category_on_bd)
# #         if success == False:
# #             return

# # path = "C:\\Git\\fala\\wong\\text\\url.txt" #  WINDOWS
# # #th = "wong//text//url.txt" # MAC OR LINUX


# web = open(config("OH_TEXT_PATH"),"r").readlines()
# links = []
# for url in web:
  
#     links.append(url.rstrip())



# webs = []
# for i,v in enumerate(links):
#     for e in range (200):

#         a=v+str(e+1)
 
#         webs.append(a)



# def oh_scrapping ():

#     for id, val  in enumerate (webs):

#         scrapping = scrap(val)
#         print(scrapping)
#         print(val)
#         if scrapping == False:
#             continue
        
     
                
            
# oh_scrapping() 


# #scrap("https://www.oechsle.pe/tecnologia/televisores?&optionOrderBy=OrderByScoreDESC&O=OrderByScoreDESC&page=14")





