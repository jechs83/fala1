
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from datetime import date
import sys
import time
current_time= time.strftime("%H:%M")
sys.path.append('/Users/javier/GIT/fala') 
from g_var import mongo_db,path_ripley_links,path_ripley_links2,path_ripley_links3,path_ripley_links4,path_ripley_links5,path_ripley_links6
date = date.today()
current_date= date.strftime("%d/%m/%Y")
client = MongoClient(mongo_db)

def scrap (web):

    proxies = {
        "http":"http://202.21.110.82:8020"
        }

    res=requests.get(web,  proxies= proxies)
    print("Respuesta del servidor :"+str(res.status_code))
    #res=requests.get(url,  headers=headers)

    soup = BeautifulSoup(res.text, "html.parser")

  
    element = soup.find("div", class_="catalog-products-container")


    for i in element():
        print("##################################################")
        try:
          product = i.find("button", class_="btn-add-car" ).attrs.get("name")
        except: product = "Null"
        try:
         image = i.find("img" ).attrs.get("src")
        except: image = "Null"
        print(image)
        print(product)
      
 


  
    #print(soup.title.text)

scrap("https://juntoz.com/catalogo?categoryId=1409&top=28&skip=56&orderBy=rating-desc")