from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by  import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from pymongo import MongoClient
from datetime import date
import sys
sys.path.append('/Users/javier/GIT/fala') 
import sys
import time
from wong.g_var import mongo_db
current_time= time.strftime("%H:%M")
date = date.today()
current_date= date.strftime("%d/%m/%Y")
import time
current_time= time.strftime("%H:%M")


client = MongoClient(mongo_db)

options = Options()
options.add_argument('log-level=3')
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

firstSku = None
pages = None

def shop():
    global firstSku
    elements=driver.find_elements(By.XPATH,"//div[contains(@class,'prod-result')]/div/ul/li/div/div")
    for idx, i in enumerate(elements):
        try:
            driver.find_element(By.XPATH,"//body/div[3]/div[1]/div[1]/div[1]/span[1]/span[1]/i[1]").click()
        except: print("cierra el maldito pop up")
        if idx == 11:
              try:
                  driver.find_element(By.XPATH,"//body/div[3]/div[1]/div[1]/div[1]/span[1]/span[1]/i[1]").click()
              except: print( "pop up se cierra")
              driver.execute_script("window.scrollTo(0,2000)"); time.sleep(1)
              driver.execute_script("window.scrollTo(0,3000)");time.sleep(1)
        if idx ==20:
            try:
                  driver.find_element(By.XPATH,"//body/div[3]/div[1]/div[1]/div[1]/span[1]/span[1]/i[1]").click()
            except: print("cierra el maldito pop up")
            driver.execute_script("window.scrollTo(0,8000)");time.sleep(1)
        try:
         sku=i.get_attribute("data-sku")
         #print(sku)
         if idx == 0:
                #print("se imprimer el primer sku")
            #print(firstSku)
            #print(sku)
            if firstSku == sku:
                return True
            firstSku = sku
        
        except: sku ="Null"
        if sku=="Null":
            continue
        
        #seller=i.get_attribute("data-seller")
        seller="promart"
        
        try:
         product_category=i.get_attribute("data-category")
        except: product_category = "Null"
        try:
         brand=i.find_element(By.XPATH, "//div[contains(@class,'prod-result')]/div/ul/li["+str(idx+1)+"]/div/div//div[@class='brand js-brand']").text
        except:brand="Null"
        try:
         product=i.find_element(By.XPATH, "//body/div[@id='content']/section[1]/section[1]/div[3]/div[1]/div[1]/div[2]/div[3]/div[2]/div[1]/div[1]/div[1]/ul[1]/li["+str(idx+1)+"]/div[1]/div[1]/div[8]/h3[1]").text
        except: product="Null"
        try:
         link = i.find_element(By.XPATH,"//body/div[@id='content']/section[1]/section[1]/div[3]/div[1]/div[1]/div[2]/div[3]/div[2]/div[1]/div[1]/div[1]/ul[1]/li["+str(idx+1)+"]/div[1]/div[1]/div[8]/h3[1]/a[1]").get_attribute("href")
        except:link="Null"
        try:
         img = i.find_element(By.XPATH, "//body/div[@id='content']/section[1]/section[1]/div[3]/div[1]/div[1]/div[2]/div[3]/div[2]/div[1]/div[1]/div[1]/ul[1]/li["+str(idx+1)+"]/div[1]/div[1]/a[2]/img[1]").get_attribute('src')
        except:img="Null"
    
        try:
             list_price =i.get_attribute("data-list-price")
             list_price=list_price.split(" ")
             list_price=list_price[1].split("\n")
             list_price=list_price[0].replace(",","")
        except: list_price=0
        try:
            best_price=i.get_attribute("data-best-price")
            best_price=best_price.split(" ")
            best_price=best_price[1].split("\n")
            best_price=best_price[0].replace("S/. ","").replace(",","")
            
        except: best_price=0

        try:
            card_price= i.find_element(By.XPATH,"//body/div[@id='content']/section[1]/section[1]/div[3]/div[1]/div[1]/div[2]/div[3]/div[2]/div[1]/div[1]/div[1]/ul[1]/li["+str(idx+1)+"]/div[1]/div[1]/div[8]/div[5]/div[2]/span[2]/span[1]").text
            #card_price = i.get_attribute("data-pricetoh")
            card_price=card_price.replace(",","")
            # if card_price == "-":
            #      card_price=0
        except: card_price=0

        try:
            web_dsct=i.find_element(By.XPATH,"//body/div[@id='content']/section[1]/section[1]/div[3]/div[1]/div[1]/div[2]/div[3]/div[2]/div[1]/div[1]/div[1]/ul[1]/li["+str(idx+1)+"]/div[1]/div[1]/div[6]/p[1]").text
            web_dsct= web_dsct.split("\n")
            web_dsct=web_dsct[1].replace("-","").replace("%","")
        except: web_dsct =0

        try:
         card_dsct=i.find_element(By.XPATH, "//body/div[@id='content']/section[1]/section[1]/div[3]/div[1]/div[1]/div[2]/div[3]/div[2]/div[1]/div[1]/div[1]/ul[1]/li["+str(idx+1)+"]/div[1]/div[1]/div[6]/div[1]").text
         card_dsct=card_dsct.replace("-","").replace("%","")
        except: card_dsct =0
        market = "promart"
        db = client["shopstar"]
        collection = db["promart"]

        
        x = collection.find_one({"_id":market+sku})
        try:
                if x:
                    filter = {"_id":market+sku}
                    newvalues = { "$set":{ 

                    "_id":market+sku, 
                    "brand":brand,
                    "sku":sku,
                    "market":market,
                    "product": product,
                    "list_price":float(list_price),           
                    "best_price":float(best_price),
                    "card_price":float(card_price),
                    "web_dsct":float(web_dsct),
                    "card_dsct":float(card_dsct),
                    "category":product_category,
                    "link": str(link),
                    "image":str(img),
                    "date":current_date,
                    "time":current_time,
                    "seller":seller
                    }}
                    collection.update_one(filter,newvalues)
                else:
                    data =  {
                    "_id":market+sku, 
                    "brand":brand,
                    "sku":sku,
                    "market":market,
                    "product": product,
                    "list_price":float(list_price),           
                    "best_price":float(best_price),
                    "card_price":float(card_price),
                    "web_dsct":float(web_dsct),
                    "card_dsct":float(card_dsct),
                    "category":product_category,
                    "link": str(link),
                    "image":str(img),
                    "date":current_date,
                    "time":current_time,
                    "seller":seller
                        }
                    collection.insert_one(data)
        except:print("no se pudo meter registro")

        print("product number "+ str(idx+1));print("Marca: "+brand);print("Producto: "+product);print("Vendedor: "+seller);print("SKU: "+sku);print("Catgeoria: "+product_category);print("Precio Lista: "+str(list_price));print("Precio Online: "+str(best_price));print("Precio Tarjeta "+str(card_price));
        print("Dsct web: "+str(web_dsct));print("Dsct card: "+str(card_dsct));print("Imagen: "+img);print("Url: "+link);print("##################");print()

    try: 
        driver.find_element(By.XPATH, "//a[@id='next_link']").click()
    except: 
        print("no next page")
        return True; 
    time.sleep(4)
        

# def next_page():
#         global pages
        
#         print(pages)
#         time.sleep(4)



def scrapero(web):

    driver.get(web)
    time.sleep(3)
    try:
     driver.find_element(By.XPATH,"//body/div[3]/div[1]/div[1]/div[1]/span[1]/span[1]/i[1]").click()
    except: print("cierra el maldito pop up")
    for i in range(700):
        global pages

        scrap=shop()
    
        print(web+str(i+1))
        if scrap == True:
            return True
        pages=i+1
    driver.quit()
    print("se cierra el driver")

################################################################################################################
################################################################################################################

array_tec=[]

arg_ = sys.argv[1]

f = open(arg_, "r")
x = f.readlines()

for i in x:
   array_tec.append(i.rstrip())   

for i in (list(array_tec)):   

    x = scrapero(i)
    if x == True:
        continue
            
     


