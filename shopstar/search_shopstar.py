from unicodedata import category
from selenium import webdriver
import sys
sys.path.append('/Users/javier/GIT/fala') 
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
from wong.g_var import mongo_db
date = date.today()
current_day= date.strftime("%d/%m/%Y")

client = MongoClient(mongo_db)


web = "https://shopstar.pe/buscapagina?ft=promart&PS=24&sl=980125a2-9928-4068-912c-83001d75bb51&cc=24&sm=0&PageNumber=2"
options = Options()
options.add_argument("--ignore-ssl-errors")
options.add_argument('log-level=3')
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(web)
time.sleep(4)

def shopstar(cat):
   for i in range (25):
      if i ==0: continue
      if i == 12:
        driver.execute_script("window.scrollTo(0,2000)")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0,3000)")
        time.sleep(2)

      brand= driver.find_element(By.XPATH,"//body/div[4]/div[6]/section[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/ul[1]/li["+str(i)+"]/div[1]/div[3]/h6[1]/strong[1]").text
      product = driver.find_element(By.XPATH,"/html[1]/body[1]/div[4]/div[6]/section[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/ul[1]/li["+str(i)+"]/div[1]/div[3]/h6[2]/a[1]").text
      try:
             list_price=driver.find_element(By.XPATH,"//body/div[4]/div[6]/section[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/ul[1]/li["+str(i)+"]/div[1]/div[3]/span[2]").text
             list_price=list_price.split(" ")
             list_price=list_price[1].split("\n")
             list_price=list_price[0].replace(",","")
      except: list_price=0
      try:
       best_price=driver.find_element(By.XPATH,"/html[1]/body[1]/div[4]/div[6]/section[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/ul[1]/li["+str(i)+"]/div[1]/div[3]/span[1]/strong[1]").text
       best_price=best_price.split(" ")
       best_price=best_price[1].replace(",","")
      except: best_price=0
      try:
       card_price= driver.find_element(By.XPATH,"//body/div[4]/div[6]/section[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/ul[1]/li["+str(i)+"]/div[1]/div[3]/div[1]").text
       card_price=card_price.split(" ")
       card_price=card_price[0].split("\n")
       card_price=card_price[0].replace("S/","").replace(",","")
      except: card_price = 0
      

      try:
       img= driver.find_element(By.XPATH,"/html[1]/body[1]/div[4]/div[6]/section[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/ul[1]/li["+str(i)+"]/div[1]/div[2]/a[1]/img[1]").get_attribute("src")
      except: img = "None"

      link= driver.find_element(By.XPATH,"//body/div[4]/div[6]/section[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/ul[1]/li["+str(i)+"]/div[1]/div[2]/a[1]").get_attribute("href")
      sku= driver.find_element(By.XPATH,"/html[1]/body[1]/div[4]/div[6]/section[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/ul[1]/li["+str(i)+"]").get_attribute("data-sku")
      market = "shop"
      category = cat
      

      print(brand); print(product); print(list_price);  print(best_price); print(card_price)
      print(img); print(link); print(current_day);print(sku)
      print("###")
      #print(sku)
      print()
      db = client["shopstar"]
      collection = db["test"]
      x = collection.find_one({"_id":market+sku})

      if x:
            filter = {"_id":market+sku}
            newvalues = { "$set":{ 

            "brand":brand,
            "sku":int(sku),
            "market":market,
            "product": product,
            "list_price":float(list_price),
            "best_price":float(best_price),
            "card_price":float(card_price),
            "category":category,
            "link": str(link),
            "image":str(img),
            "date":current_day
            }}
            collection.update_one(filter,newvalues)
      else:
            data =  {
            "_id":market+sku, 
            "brand":brand,
            "sku":int(sku),
            "markety":market,
            "product": product,
            "list_price":float(list_price),           
            "best_price":float(best_price),
            "card_price":float(card_price),
            "category":category,
            "url": str(link),
            "image":str(img),
            "date":current_day
                }
            collection.insert_one(data)


   
def next_page():
      driver.find_element(By.XPATH,"/html[1]/body[1]/div[4]/div[6]/section[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/ul[1]/li[9]/a[1]").click()


def pages():
       shopstar("varios")
       next_page()
       time.sleep(6)


for i in range(700):
       pages()
       print("page number "+str(i))
# for e in ele2:
  
#    print(e.text)



 



 


