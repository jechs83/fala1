import requests
from bs4 import BeautifulSoup, Tag
from pymongo import MongoClient
import json
from wong.g_var import mongo_db


client = MongoClient(mongo_db)

def scrap(category_url, category_on_bd):

    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"}
    res=requests.get(category_url,  headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    
    try:
      no_page = soup.find("div", class_="jsx-860724461 information-box-container")
    except:
        no_page=None
    print(no_page)
    if no_page != None:
        return False
    
    json_string = soup.find("script", id="__NEXT_DATA__").text
    json_parsed= json.loads(json_string)
    json_data= json_parsed["props"]["pageProps"]["results"]
    print("################################################")


    count=0
    for e in json_data:
        count +=1
  
       
        print("product number  "+ str(count))
        try:
            brand= e["brand"]  ## MARCA DE PRODUCTO
        except: brand=None
        
        product = e["displayName"]  ## DESCRIPCION DEL PRODUCTO
        sku= e["skuId"]             ## CODIGO DEL PRODUCTO WEB
        seller = e["sellerName"]    ## VENDEDOR DEL MARKET PLACE
        url = e["url"]              ## LINK DEL PRODUCTO
              
        try:
            img = e["mediaUrls"]     ## IMAGENES DEL PRODUCTO
            img=img[0]      
        except: img=img
        
        try:
            list_price= e["prices"][1]["price"][0]  ## PRECIO DE LISTA
            list_price= list_price.replace(",","")
        except: list_price = 0
        
        try:
            best_price= e["prices"][0]["price"][0]   ## PRECIO DE OFERTA ONLINE
            best_price=  best_price.replace(",","")
        except: best_price= 0
        
        try:
            card_price=e["prices"][2]["price"][0]     ## PRECIO CON TARJETA
            card_price= card_price.replace(",","")
        except: card_price=0
        
        category = category_on_bd
        print(brand); print(category);print(product); print(sku);print(seller); print("Precio de lista "+str(list_price)); print("Precio de online "+str(best_price));
        print("Precio con tarjeta "+str(card_price)); print(url); print(img); print()
        
        db = client["falabella"]
        collection = db["test"]
        x = collection.find_one({"_id":sku})

        if x:
            filter = {"_id":sku}
            newvalues = { "$set":{ 

            "brand":brand,
            "seller":seller,
            "product": product,
            "list_price":float(list_price),
            "card_price":float(card_price),
            "category":category_on_bd,
            "url": str(url),
            "image": str(img)
            }}
            collection.update_one(filter,newvalues)
        else:
            data =  {
            "_id":sku, 
            "brand":brand,
            "seller":seller,
            "product": product,
            "list_price":float(list_price),
            "best_price":float(best_price),
            "card_price":float(card_price),
            "category":category_on_bd,
            "url": str(url),
            "image": str(img)
                }
            collection.insert_one(data)
    return True

def scrap_category(category_url, category_on_bd):
    for i in range(250):
        success = scrap(category_url+str(i+1), category_on_bd)
        if success == False:
            return

###########################################################

for id, val in enumerate(fala):
  
  web = val[0];  cat = val[1]

  scrap_category(web, cat) ## GENERA LA LISTA DE PAGINACIONES POR CATEGORIA
  print(web)
  print(cat)