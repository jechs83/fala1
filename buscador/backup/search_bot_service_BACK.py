import sys
import time
from html_test import html_code
import gc
from pymongo import MongoClient
import itertools
import re
import base64
import requests
import pymongo
from bd_compare import save_data_to_mongo_db
from decouple import config
from datetime import datetime
import telegram
from pandas import DataFrame
import pytz
from datetime import datetime

server_date = datetime.now()
timezone = pytz.timezone("America/Bogota")
peru_date = server_date.astimezone(timezone)

from pymongo import MongoClient
from decouple import config
client = MongoClient(config("MONGO_DB"))
#date = peru_date.strftime("%d/%m/%Y" )
#oferta_telegram = "👉 https://t.me/OfertasDescuentosPeru1 👈"
oferta_telegram = ""

#https://api.telegram.org/bot5573005249:AAFGCjc7zuI1XoHMqbd6gr1I1ZVi9Xd2I9s/sendMessage


def dia():
    now = datetime.now()
    date = now.strftime("%d/%m/%Y")
    #date = date.today()
    return date

date = dia()


def send_telegram(message,foto, bot_token, chat_id):

    if not foto:
        foto="https://image.shutterstock.com/image-vector/no-image-available-sign-absence-260nw-373243873.jpg"
    
    if len(foto)<=4:
            foto="https://image.shutterstock.com/image-vector/no-image-available-sign-absence-260nw-373243873.jpg"

    response = requests.post(
        
        f'https://api.telegram.org/bot{bot_token}/sendPhoto',
        data={'chat_id': chat_id, 'caption': str(message), "parse_mode": "HTML"},
        files={'photo': requests.get(foto).content},
    
        )

def send_document(document,bot_token, chat_id):
    # Create a bot instance using your bot token
    bot = telegram.Bot(token=bot_token)

    # Send a document to the chat with ID `chat_id`
    bot.send_document(chat_id=chat_id, document=open(document, 'rb'))

########################################################################
########################################################################
########################################################################

def send_telegram2(message, foto, html_file, bot_token, chat_id):
    # Read the contents of the photo file
    photo_contents = requests.get(foto).content

    # Read the contents of the HTML file
    with open(html_file, 'rb') as f:
        html_contents = f.read()

    # Encode the HTML file as base64
    encoded_html = base64.b64encode(html_contents).decode()

    # Combine the photo and HTML contents into a single message
    html_text = f'<a href="data:text/html;base64,{encoded_html}">Click aqui para ver Precios Historicos</a>'
    message_text = f'{message}\n\n{html_text}'

    # Send the combined message using the sendPhoto and sendDocument methods
    response1 = requests.post(
        f'https://api.telegram.org/bot{bot_token}/sendPhoto',
        data={'chat_id': chat_id, 'caption': message_text, "parse_mode": "HTML"},
        files={'photo': photo_contents},
        
    )

    response2 = requests.post(
        f'https://api.telegram.org/bot{bot_token}/sendDocument',
        data={'chat_id': chat_id},
        files={'document': ('historico.html', html_contents, 'text/html')}
    )

# Example usage

def send_telegram3(message, foto, html_file, bot_token, chat_id):
    # Read the contents of the photo file
    photo_contents = requests.get(foto).content

    # Read the contents of the HTML file
    with open(html_file, 'rb') as f:
        html_contents = f.read()

    # Encode the HTML file as base64
    encoded_html = base64.b64encode(html_contents).decode()

    # Create a multipart/form-data payload with three parts
    payload = {
        'chat_id': chat_id,
        'caption': message,
        'parse_mode': 'HTML',
        'photo': photo_contents,
        'document': ('historico.html', html_contents, 'text/html'),
    }

    # Send the message using the multipart/form-data payload
    response = requests.post(
        f'https://api.telegram.org/bot{bot_token}/sendPhoto',
        files=payload
    )

########################################################################
########################################################################
########################################################################

    # requests.post("https://api.telegram.org/bot"+str(bot_token)+"/sendMessage",
            
    # data= {'chat_id': chat_id ,'text': str(message) , 'parse_mode':ParseMode.HTML}  ) # DISC0VERY
    
# def send_telegram_photo(foto, bot_token, chat_id):
#    response = requests.post(
#     f'https://api.telegram.org/bot{bot_token}/sendPhoto',
#     data={'chat_id': chat_id},
#     files={'photo': requests.get(foto).content},
# )


    

client = MongoClient(config("MONGO_DB"))
db5 = client["scrap"]
collection5 = db5["scrap"] 



### BUSQUEDA CON COD

def busqueda(codigo,bot_token, chat_id):
    print("entro a busqueda de codigo")
    #db5.command({"planCacheClear": "scrap"})
    t5 = collection5.find({"sku":str(codigo), "date":date})

    print( "se realizo busqueda")
    print(codigo)
    for i in t5:
        print("se envio a telegram")    
        if  i["card_price"] == 0:
                card_price = ""
        else:
            card_price = '\n👉Precio Tarjeta :'+str(i["card_price"])

        if i["list_price"] == 0:
                list_price = ""
        else:
            list_price = '\n\n➡️Precio Lista :'+str(i["list_price"])
        if i["web_dsct"] <= 50:
            dsct = "🟡"
        if i["web_dsct"] > 50 and i["web_dsct"]  <=69:
            dsct = "🟢"
        if i["web_dsct"] >=70:
            dsct = "🔥🔥🔥🔥🔥🔥"
    

        msn =  "✅Marca: "+str(i["brand"])+"\n✅"+str(i["product"])+list_price+"\n👉Precio web :"+str(i["best_price"])+card_price+"\n"+dsct+"Descuento: "+"% "+str(i["web_dsct"])+"\n"+"\n\n⌛"+i["date"]+" "+ i["time"]+"\n🔗Link :"+str(i["link"])+"\n🏠home web:"+i["home_list"]+"\n\n◀️◀️◀️◀️◀️◀️◀️▶️▶️▶️▶️▶️▶️"
        
        foto = i["image"]

        send_telegram(msn, foto, bot_token, chat_id)
       


def search_brand_dsct(brand,dsct, bot_token, chat_id):
    #db5.command({"planCacheClear": "scrap"})
    print
    print(bot_token)
    print(chat_id)
    brand = str(brand).replace("%"," ")
    if dsct <41:
        dsct = 40
    t5 = collection5.find({"brand":{"$in":[ re.compile(str(brand), re.IGNORECASE)]}, "web_dsct":{"$gte":int(dsct)}, "date": date})

    print( "se realizo busqueda")

    count = 0
    for i in t5:
        # count = count+1
        # if count == 100:
        #     break
        print(i)
        print("se envio a telegram")   
        if  i["card_price"] == 0:
                card_price = ""
        else:
            card_price = '\n👉Precio Tarjeta :'+str(i["card_price"])

        if i["list_price"] == 0:
                list_price = ""
        else:
            list_price = '\n\n➡️Precio Lista :'+str(i["list_price"])

        if i["web_dsct"] <= 50:
            dsct = "🟡"
        if i["web_dsct"] > 50 and i["web_dsct"]  <=69:
            dsct = "🟢"
        if i["web_dsct"] >=70:
            dsct = "🔥🔥🔥🔥🔥🔥"
        
        # try:
        #     historic = minimo(i["sku"])[3]
        # except:
        #     historic = False
        # print(historic)

        # if historic == True:

        #     historic_min = "\n🔥🔥🔥🔥🔥🔥🔥 Minimo historico"
        #     historic_list = "\nPrecio minimo: "+str(minimo(i["sku"])[0])+"\n"+"Precio anterior: "+str(minimo(i["sku"])[1])+"\n"+"Precio maximo: "+str(minimo(i["sku"])[2])
        # if historic == False:

        # historic_min = ""
        # historic_list=""
   

        msn =  "✅Marca: "+str(i["brand"])+"\n✅"+str(i["product"])+list_price+"\n👉Precio web :"+str(i["best_price"])+card_price+"\n"+dsct+"Descuento: "+"% "+str(i["web_dsct"])+"\n"+"\n\n⌛"+i["date"]+" "+ i["time"]+"\n🔗Link :"+str(i["link"])+"\n🏠home web:"+i["home_list"]+"\n\n◀️◀️◀️◀️◀️◀️◀️▶️▶️▶️▶️▶️▶️"
        
        foto = i["image"]
  

        if not foto:

            foto="https://image.shutterstock.com/image-vector/no-image-available-sign-absence-260nw-373243873.jpg"

        send_telegram(msn, foto, bot_token, chat_id)
        time.sleep(1)
    gc.collect()
        


def search_market_dsct(market,dsct, bot_token, chat_id):
    db5.command({"planCacheClear": "scrap"})

    if dsct <41:
        dsct = 40
    t5 = collection5.find({"market":market, "web_dsct":{"$gte":int(dsct)}, "brand":{"$nin":[re.compile("generica", re.IGNORECASE), 
                            re.compile("generico", re.IGNORECASE),  re.compile("genérico", re.IGNORECASE), 
                            re.compile("genérica", re.IGNORECASE),  re.compile("generic", re.IGNORECASE)] }, "date": date})

    print("se busca en base de datos")
 

    for i in t5:
   
        if  i["card_price"] == 0:
            card_price = ""
        else:
            card_price = '\n👉Precio Tarjeta :'+str(i["card_price"])

        if i["list_price"] == 0:
                list_price = ""
        else:
            list_price = '\n\n➡️Precio Lista :'+str(i["list_price"])

        if i["web_dsct"] <= 50:
            dsct = "🟡"
        if i["web_dsct"] > 50 and i["web_dsct"]  <=69:
            dsct = "🟢"
        if i["web_dsct"] >=70:
            dsct = "🔥🔥🔥🔥🔥🔥"

        # try:
        #     historic = minimo(i["sku"])[3]
        # except:
        #     historic = False
        # print(historic)

        # if historic == True:
        #     historic_min = "\n🔥🔥🔥🔥🔥🔥🔥 Minimo historico"
        #     historic_list = "\nPrecio minimo: "+str(minimo(i["sku"])[0])+"\n"+"Precio anterior: "+str(minimo(i["sku"])[1])+"\n"+"Precio maximo: "+str(minimo(i["sku"])[2])
        # if historic == False:
        #     historic_min = ""
        #     historic_list=""
        historic_min = ""
        historic_list=""

        msn =  "✅Marca: "+str(i["brand"])+"\n✅"+str(i["product"])+list_price+"\n👉Precio web :"+str(i["best_price"])+card_price+"\n"+dsct+"Descuento: "+"% "+str(i["web_dsct"])+"\n"+"\n\n⌛"+i["date"]+" "+ i["time"]+"\n🔗Link :"+str(i["link"])+"\n🏠home web:"+i["home_list"]+"\n\n◀️◀️◀️◀️◀️◀️◀️▶️▶️▶️▶️▶️▶️"

        
        foto = i["image"]
      
        send_telegram (msn, foto, bot_token, chat_id)
        time.sleep(1)
        print("Se envio mensaje a telegram")
    gc.collect()



def  search_market_dsct_antitopo(market, dsct, dsct2, bot_token ,chat_id):
    db5.command({"planCacheClear": "scrap"})
    print
    print(bot_token)
    print(chat_id)
    
    if dsct <41:
        dsct = 40
    t5 = collection5.find({"market":market, "web_dsct":{"$gte":int(dsct),"$lte":int(dsct2) }, "brand":{"$nin":[re.compile("generica", re.IGNORECASE), 
                            re.compile("generico", re.IGNORECASE),  re.compile("genérico", re.IGNORECASE), 
                            re.compile("genérica", re.IGNORECASE),  re.compile("generic", re.IGNORECASE)] }, "date": date})
   
    print( "se realizo busqueda")

    count = 0
    for i in t5:
        # count = count+1
        # if count == 100:
        #     break
        # print(i)
        print("se envio a telegram")  
        if  i["card_price"] == 0:
                card_price = ""
        else:
            card_price = '\n👉Precio Tarjeta :'+str(i["card_price"])

        if i["list_price"] == 0:
                list_price = ""
        else:
            list_price = '\n\n➡️Precio Lista :'+str(i["list_price"])

        if i["web_dsct"] <= 50:
            dsct = "🟡"
        if i["web_dsct"] > 50 and i["web_dsct"]  <=69:
            dsct = "🟢"
        if i["web_dsct"] >=70:
            dsct = "🔥🔥🔥🔥🔥🔥"

        # try:
        #     historic = minimo(i["sku"])[3]
        # except:
        #     historic = False
        # print(historic)

        # if historic == True:

        #     historic_min = "\n🔥🔥🔥🔥🔥🔥🔥 Minimo historico"
        #     historic_list = "\nPrecio minimo: "+str(minimo(i["sku"])[0])+"\n"+"Precio anterior: "+str(minimo(i["sku"])[1])+"\n"+"Precio maximo: "+str(minimo(i["sku"])[2])
        # if historic == False:

        historic_min = ""
        historic_list=""

        msn =  "✅Marca: "+str(i["brand"])+"\n✅"+str(i["product"])+list_price+"\n👉Precio web :"+str(i["best_price"])+card_price+"\n"+dsct+"Descuento: "+"% "+str(i["web_dsct"])+"\n"+"\n\n⌛"+i["date"]+" "+ i["time"]+"\n🔗Link :"+str(i["link"])+"\n🏠home web:"+i["home_list"]+"\n\n◀️◀️◀️◀️◀️◀️◀️▶️▶️▶️▶️▶️▶️"

        
        foto = i["image"]
        send_telegram (msn, foto, bot_token, chat_id)   
        # msn =  "<b>Marca: "+str(i["brand"])+"</b>\nModelo: "+str(i["product"])+"\nPrecio Lista :"+str(i["list_price"])+"\n<b>Precio web :"+str(i["best_price"])+"</b>\nPrecio Tarjeta :"+str(i["card_price"])+"\n"+"Descuento: "+"%"+str(i["web_dsct"])+"\n"+i["date"]+" "+ i["time"]+"\n"+str(i["image"])+"\n\nLink :"+str(i["link"])+"\nhome web:"+i["home_list"]
        # send_telegram (msn, bot_token, chat_id)
        time.sleep(1)
    gc.collect()


t1 =  collection5.find( {"web_dsct":{ "$gte":70},"date":date ,"brand":{"$in":[ 
re.compile("samsung", re.IGNORECASE),re.compile("lenovo", re.IGNORECASE),re.compile("Lg", re.IGNORECASE),
re.compile("Asus", re.IGNORECASE),re.compile("Xiaomi", re.IGNORECASE),re.compile("indurama", re.IGNORECASE),
re.compile("oster", re.IGNORECASE),re.compile("bosch", re.IGNORECASE),re.compile("acer", re.IGNORECASE),
re.compile("huawei", re.IGNORECASE),re.compile("panasonic", re.IGNORECASE),re.compile("winnia", re.IGNORECASE),
re.compile("phillips", re.IGNORECASE),re.compile("mabe", re.IGNORECASE),re.compile("nex", re.IGNORECASE),
re.compile("hyundai", re.IGNORECASE),re.compile("tcl", re.IGNORECASE),re.compile("monark ", re.IGNORECASE),
re.compile("goliat ", re.IGNORECASE),re.compile("oxford ", re.IGNORECASE),re.compile("jafi-bike ", re.IGNORECASE),
re.compile("besatti ", re.IGNORECASE),re.compile("altitude ", re.IGNORECASE),re.compile("trek ", re.IGNORECASE),
re.compile("advantech ", re.IGNORECASE),re.compile("ecoride", re.IGNORECASE),re.compile("izytek", re.IGNORECASE),
re.compile("movimiento", re.IGNORECASE),re.compile("xclusive", re.IGNORECASE),re.compile("cross", re.IGNORECASE),
re.compile("jvc", re.IGNORECASE),re.compile("motorola", re.IGNORECASE),re.compile("bgh", re.IGNORECASE),
re.compile("hisense", re.IGNORECASE),re.compile("blackline", re.IGNORECASE),re.compile("daewoo", re.IGNORECASE),
re.compile("dell", re.IGNORECASE),re.compile("hp", re.IGNORECASE),re.compile("honor", re.IGNORECASE),re.compile("advance", re.IGNORECASE),re.compile("gigabyte", re.IGNORECASE),re.compile("msi", re.IGNORECASE),re.compile("vastec", re.IGNORECASE),re.compile("xpg", re.IGNORECASE),re.compile("alienware", re.IGNORECASE),re.compile("SENNHEISER", re.IGNORECASE),re.compile("HIKVISION", re.IGNORECASE),re.compile("logitech", re.IGNORECASE),re.compile("EZVIZ", re.IGNORECASE),re.compile("BEHRINGER", re.IGNORECASE),re.compile("googledji", re.IGNORECASE),re.compile("best", re.IGNORECASE),re.compile("amazon", re.IGNORECASE),re.compile("sonos", re.IGNORECASE),re.compile("TP LINK", re.IGNORECASE),re.compile("razer", re.IGNORECASE),re.compile("UMIDIGI", re.IGNORECASE),re.compile("vivo", re.IGNORECASE),re.compile("oppo", re.IGNORECASE),re.compile("kingston", re.IGNORECASE),re.compile("sonoff", re.IGNORECASE),re.compile("makita", re.IGNORECASE),re.compile("thomas", re.IGNORECASE),re.compile("baseus", re.IGNORECASE),re.compile("karcher", re.IGNORECASE),re.compile("stanley", re.IGNORECASE),re.compile("BLACK AND DECKER", re.IGNORECASE),re.compile("BLACK & DECKER", re.IGNORECASE),re.compile("dewalt", re.IGNORECASE),re.compile("skil", re.IGNORECASE),re.compile("bauker", re.IGNORECASE),re.compile("uberman", re.IGNORECASE),re.compile("fujifilm", re.IGNORECASE),re.compile("nikonaiwa", re.IGNORECASE),re.compile("microsoft", re.IGNORECASE),re.compile("tp-link", re.IGNORECASE),re.compile("fuji", re.IGNORECASE),re.compile("ADIDAS", re.IGNORECASE),re.compile("ASICS", re.IGNORECASE),re.compile("NEW BALANCE", re.IGNORECASE),re.compile("nike", re.IGNORECASE),re.compile("puma", re.IGNORECASE),re.compile("reebok", re.IGNORECASE),re.compile("skechers", re.IGNORECASE),re.compile("under armour", re.IGNORECASE),re.compile("umbro", re.IGNORECASE),re.compile("Clementoni", re.IGNORECASE),re.compile("vainsa", re.IGNORECASE),re.compile("ibm", re.IGNORECASE),re.compile("lego", re.IGNORECASE),re.compile("intel", re.IGNORECASE),re.compile("louis vuitton", re.IGNORECASE),re.compile("prada", re.IGNORECASE),re.compile("pampers", re.IGNORECASE),re.compile("zara", re.IGNORECASE),re.compile("canon", re.IGNORECASE),re.compile("caterpillar", re.IGNORECASE),re.compile("nintendo", re.IGNORECASE),re.compile("rolex", re.IGNORECASE),re.compile("nokia", re.IGNORECASE),re.compile("lexus", re.IGNORECASE),re.compile("exxon mobil", re.IGNORECASE),re.compile("ralph lauren", re.IGNORECASE),re.compile("apple", re.IGNORECASE),re.compile("chicco", re.IGNORECASE),re.compile("safety", re.IGNORECASE),re.compile("cosco", re.IGNORECASE),re.compile("infanti", re.IGNORECASE),re.compile("fisher price", re.IGNORECASE),re.compile("Hot wheels", re.IGNORECASE),re.compile("cry babies", re.IGNORECASE),re.compile("my little pony", re.IGNORECASE),re.compile("Baby alive", re.IGNORECASE),re.compile("index", re.IGNORECASE),re.compile("barbie", re.IGNORECASE),re.compile("Avent", re.IGNORECASE),re.compile("Baby Club Chic", re.IGNORECASE),re.compile("Baby Harvest", re.IGNORECASE),re.compile("Baby liss", re.IGNORECASE),re.compile("Babycottons", re.IGNORECASE),re.compile("Barbados", re.IGNORECASE),re.compile("basemet", re.IGNORECASE),re.compile("Bata", re.IGNORECASE),re.compile("Bblubs", re.IGNORECASE),re.compile("Blackout", re.IGNORECASE),re.compile("BORN", re.IGNORECASE),re.compile("Bosse", re.IGNORECASE),re.compile("Bronco", re.IGNORECASE),re.compile("Bubble gummers", re.IGNORECASE),re.compile("cacharel", re.IGNORECASE),re.compile("Carters", re.IGNORECASE),re.compile("caterpilla", re.IGNORECASE),re.compile("Champion", re.IGNORECASE),re.compile("Cloudbreak", re.IGNORECASE),re.compile("Colloky", re.IGNORECASE),re.compile("columbia", re.IGNORECASE),re.compile("crocs", re.IGNORECASE),re.compile("diadora", re.IGNORECASE),re.compile("Diesel", re.IGNORECASE),re.compile("DJI", re.IGNORECASE),re.compile("Drimer", re.IGNORECASE),re.compile("Drom", re.IGNORECASE),re.compile("Dunkelvolk", re.IGNORECASE),re.compile("Edufun", re.IGNORECASE),re.compile("Emma Cotton Babies", re.IGNORECASE),re.compile("Evenflo", re.IGNORECASE),re.compile("Forli", re.IGNORECASE),re.compile("Gama", re.IGNORECASE),re.compile("Gotcha", re.IGNORECASE),re.compile("Gymboree", re.IGNORECASE),re.compile("Huggies", re.IGNORECASE),re.compile("Hugo boss", re.IGNORECASE),re.compile("Jack & Jones", re.IGNORECASE),re.compile("Kansas", re.IGNORECASE),re.compile("Kayra Man", re.IGNORECASE),re.compile("lacoste", re.IGNORECASE),re.compile("Lee", re.IGNORECASE),re.compile("Levis", re.IGNORECASE),re.compile("Little mommy", re.IGNORECASE),re.compile("Little tikes", re.IGNORECASE),re.compile("Lois", re.IGNORECASE),re.compile("lotto", re.IGNORECASE),re.compile("marquis", re.IGNORECASE),re.compile("Maui and Sons", re.IGNORECASE),re.compile("merrell", re.IGNORECASE),re.compile("Mountain gear", re.IGNORECASE),re.compile("NBA", re.IGNORECASE),re.compile("New Era", re.IGNORECASE),re.compile("Next", re.IGNORECASE),re.compile("Ninebot", re.IGNORECASE),re.compile("north face", re.IGNORECASE),re.compile("North star", re.IGNORECASE),re.compile("Oakley", re.IGNORECASE),re.compile("Osh kosh", re.IGNORECASE),re.compile("Parada 111", re.IGNORECASE),re.compile("Paraiso", re.IGNORECASE),re.compile("Pionier", re.IGNORECASE),re.compile("Quiksilver", re.IGNORECASE),re.compile("Reef", re.IGNORECASE),re.compile("Robert Lewis", re.IGNORECASE),re.compile("rusty", re.IGNORECASE),re.compile("Scoop", re.IGNORECASE),re.compile("Siegen", re.IGNORECASE),re.compile("Sybilla", re.IGNORECASE),
re.compile("Tap out", re.IGNORECASE),
re.compile("Volcom", re.IGNORECASE),re.compile("Wahl", re.IGNORECASE),re.compile("Whirpool", re.IGNORECASE),
re.compile("Woallance", re.IGNORECASE), re.compile("scoop", re.IGNORECASE),    
    ]}})

pro = [t1]  ## ARREGLO DE LOS QUERYS DE MONGO PARA MANDAR POR TELEGRAM
products = []




def brand_list(ropa,cat, bot_token,chat_id):
    
    db_cat = client["scrap"]
    collection_cat = db_cat[cat]   
    db_cat.command({"planCacheClear": cat})

    t9 = collection_cat.find({})

    for i in t9:
        print(i)
        print("se envio lista ropa")      
        foto = "https://previews.123rf.com/images/ionutparvu/ionutparvu1612/ionutparvu161200410/67602131-categories-stamp-sign-text-word-logo-red.jpg"

        send_telegram ("brand",foto,bot_token, chat_id)
    gc.collect()


###############################################################################


def save_brand_to_mongodb(brand,category):

        db = client["brands"]
        collection= db[category]
        db.command({"planCacheClear": category})
      
        x = collection.find_one({"brand":brand})
      
        if x  :
            #print(" ACTUALIZA BASE DE DATOS ")
            filter = {"brand":brand}
            newvalues = { "$set":{ 
            "brand":brand}   
           
            }
            collection.update_one(filter,newvalues)            
        else:
            
            data =  {
            "brand":brand     

            }
            collection.insert_one(data)
        gc.collect()



def add_brand_list(brand,category,bot_token,chat_id):

    db = client["brands"]
    collection= db[category]
    db.command({"planCacheClear": "brands"})
    t9 = collection.find({})
    

    for i in t9:
        print(i)
        print("se envio lista ropa")      
        save_brand_to_mongodb(brand,category)
    foto = "https://previews.123rf.com/images/ionutparvu/ionutparvu1612/ionutparvu161200410/67602131-categories-stamp-sign-text-word-logo-red.jpg"

    
    send_telegram(" se grabo la Marca en la lista de busqueda  ",foto , bot_token, chat_id)
    gc.collect()



def delete_brand(brand,category,bot_token,chat_id):
    
    brand = brand.replace("%"," ")
    db = client["brands"]
    collection= db[category]
    collection.delete_one({"brand":brand})
    foto = "https://previews.123rf.com/images/ionutparvu/ionutparvu1612/ionutparvu161200410/67602131-categories-stamp-sign-text-word-logo-red.jpg"

    send_telegram(" se elimino la marca ingresa ", foto , bot_token, chat_id)
    gc.collect()


def read_category (bot_token,chat_id):
    categories = []
    db = client["brands"]
    for i in db.list_collection_names():
        categories.append(i)
    foto = "https://previews.123rf.com/images/ionutparvu/ionutparvu1612/ionutparvu161200410/67602131-categories-stamp-sign-text-word-logo-red.jpg"
    send_telegram( str(categories), foto, bot_token, chat_id)
    gc.collect()



def read_brands(category, bot_token,chat_id):
    db = client["brands"]
    collection= db[category]

    t9 = collection.find({})
    list_brand= []
    for i in t9:
        list_brand.append(i["brand"])

    print(list_brand)
    foto = "https://previews.123rf.com/images/ionutparvu/ionutparvu1612/ionutparvu161200410/67602131-categories-stamp-sign-text-word-logo-red.jpg"

    send_telegram( str(list_brand), foto, bot_token, chat_id)
    send_telegram(" Busqueda de marcas de 70%  a  mas ", foto, bot_token, chat_id)
    gc.collect()

############################

def auto_telegram( category, ship_db1,ship_db2, bot_token, chat_id,porcentage):
    
    print("se esta ejecutando")
    db = client["brands"]
    collection= db[category]
    t9 = collection.find({})

    collection2= db["trash"]
    t10 = collection2.find({})
    
    array_trash=[]
    array_brand= []
    product_array = []

    for i in t9:
        pattern = re.compile(i["brand"], re.IGNORECASE)
        array_brand.append(pattern)
    print(array_brand)

    for i in t10:
        pattern = re.compile(i["trash"], re.IGNORECASE)
        array_trash.append(pattern)
    print(array_trash)

    print("Esta buscando en base de datos, puede tomar un tiempo")
     
    db = client["scrap"]
    collection = db["scrap"]
    # db.command({"planCacheClear": "scrap"})


    t1 =  collection.find( {"web_dsct":{ "$gte":porcentage},"date":date ,"brand":{"$in":array_brand}, "product":{"$nin":array_trash}})
    t2 =  collection.find( {"best_price":{ "$gt": 0, "$lt": 51 },"date":date ,"brand":{"$in":array_brand}, "product":{"$nin":array_trash}})

    # Concatenate the two cursors
    result = itertools.chain(t1, t2)
    # Iterate over the result and print each document
    for i in result:
    
        product_array.append(i)
        print(i)                                                          
       
    collection_1 = db[ship_db1]
    collection_2 = db[ship_db2]

    # for i in t1:
    #     product_array.append(i)
    #     print(i)
    
    # for i in t2:
    #     product_array.append(i)
    #     print(i)



    for i in product_array:
            save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                           i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],ship_db1)
            f = print("se graba en bd datos")
            

            a= collection_1.find({"sku":i["sku"]})
            # se busca datos en offer1 cada iteracion
            a=list(a)
        
            b= collection_2.find({"sku":i["sku"]})
            # se busca datos en offer2  en cada iteracion 
            b = list(b)
            print(b)
            len_b = len(b)
            print(len_b)

            if len_b == 0:
                save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                            i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],ship_db2)
                

                if  i["card_price"] == 0:
                    card_price = ""
                else:
                    card_price = '\n👉Precio Tarjeta :'+str(i["card_price"])

                if i["list_price"] == 0:
                        list_price = ""
                else:
                    list_price = '\n\n➡️Precio Lista :'+str(i["list_price"])

                if i["web_dsct"] <= 50:
                    dsct = "🟡"
                if i["web_dsct"] > 50 and i["web_dsct"]  <=69:
                    dsct = "🟢"
                if i["web_dsct"] >=70:
                    dsct = "🔥🔥🔥🔥🔥"
                # try:
                #     historic = minimo(i["sku"])[3]
                # except:
                #     historic = False
                # print(historic)

                # if historic == True:

                #     historic_min = "\n🔥🔥🔥🔥🔥🔥🔥 Minimo historico"
                #     historic_list = "\nPrecio minimo: "+str(minimo(i["sku"])[0])+"\n"+"Precio anterior: "+str(minimo(i["sku"])[1])+"\n"+"Precio maximo: "+str(minimo(i["sku"])[2])
                # if historic == False:

                historic_min = ""
                historic_list=""
                msn =  "✅Marca: "+str(i["brand"])+"\n✅"+str(i["product"])+list_price+"\n👉Precio web :"+str(i["best_price"])+card_price+"\n"+dsct+"Descuento: "+"% "+str(i["web_dsct"])+"\n"+"\n\n⌛"+i["date"]+" "+ i["time"]+"\n🔗Link :"+str(i["link"])+"\n🏠home web:"+i["home_list"]+"\n\n◀️◀️◀️◀️◀️◀️◀️▶️▶️▶️▶️▶️▶️"

        
                foto = i["image"]
                
            
                send_telegram(msn, foto, bot_token, chat_id)
                

                print(" PRODUCTO EN BASE B NO EXISTE, SE ENVIA A TELEGRAM")
                continue


            if b!=a:
                #send_telegram( ("<b>Marca: "+i["brand"]+"</b>\nModelo: "+i["product"]+"\nPrecio Lista :" +str(i["list_price"])+ "\n<b>Precio web :"+str(i["best_price"])+"</b>\nPrecio Tarjeta :"+str(i["card_price"])+"\n"+i["image"]+"\nLink :"+str(i["link"])))
                print("PRODUCTO DE A ES DIFERENTE DE B,  SE ENVIA  A TELEGRAM")
               
                save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                            i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],ship_db2)
                continue
            if a==b:
                print("SON IGUALES,  NO SE ENVIA TELEGRAM")
    gc.collect()



def auto_telegram_total(  ship_db1,ship_db2, bot_token, chat_id,porcentage):
    print("se esta ejecutando")
    product_array = []
     
    db = client["scrap"]
    collection = db["scrap"]
    db.command({"planCacheClear": "scrap"})

    t1 =  collection.find( {"web_dsct":{ "$gte":porcentage},"date":date })

    collection_1 = db[ship_db1]
    collection_2 = db[ship_db2]

    for i in t1:
        product_array.append(i)
        print(i)

    for i in product_array:
            save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                           i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],ship_db1)
            f = print("se graba en bd datos")
            

            a= collection_1.find({"sku":i["sku"]})
            # se busca datos en offer1 cada iteracion
            a=list(a)
        
            b= collection_2.find({"sku":i["sku"]})
            # se busca datos en offer2  en cada iteracion 
            b = list(b)
            print(b)
            len_b = len(b)
            print(len_b)

            if len_b == 0:
                save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                            i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],ship_db2)
                send_telegram( ("<b>Marca: "+i["brand"]+"</b>\nModelo: "+i["product"]+"\nPrecio Lista :" +str(i["list_price"])+ "\n<b>Precio web :"+str(i["best_price"])+"</b>\nPrecio Tarjeta :"+str(i["card_price"])+"\n"+"Descuento: "+"%"+str(i["web_dsct"])+"\n"+i["date"]+" "+ i["time"]+"\n"+i["image"]+"\nLink :"+str(i["link"])+"\nhome web:"+i["home_list"])
                                ,bot_token, chat_id)
                

                print(" PRODUCTO EN BASE B NO EXISTE, SE ENVIA A TELEGRAM")
                continue


            if b!=a:
                #send_telegram( ("<b>Marca: "+i["brand"]+"</b>\nModelo: "+i["product"]+"\nPrecio Lista :" +str(i["list_price"])+ "\n<b>Precio web :"+str(i["best_price"])+"</b>\nPrecio Tarjeta :"+str(i["card_price"])+"\n"+i["image"]+"\nLink :"+str(i["link"])))
                print("PRODUCTO DE A ES DIFERENTE DE B,  SE ENVIA  A TELEGRAM")
               
                save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                            i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],ship_db2)
                continue
            if a==b:
                print("SON IGUALES,  NO SE ENVIA TELEGRAM")

    gc.collect()


##################################################################################################
##################################################################################################
def auto_telegram_between_values(  ship_db1,ship_db2, bot_token, chat_id,porcentage1, porcentage2, producto):
    print("se esta ejecutando")
    product_array = []
    
    db = client["scrap"]
    collection = db["scrap"]
    db.command({"planCacheClear": "scrap"})

    t1 =  collection.find( {"web_dsct":{ "$gte":porcentage1, "$not":{"$gte":porcentage2}},"date":date , "product":{"$not":{"$in":[re.compile(producto,re.IGNORECASE),re.compile("reloj",re.IGNORECASE) ]} } })
    collection_1 = db[ship_db1]
    collection_2 = db[ship_db2]

    for i in t1:
        product_array.append(i)
        print(i)

    for i in product_array:
            save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                           i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],ship_db1)
            f = print("se graba en bd datos")
            

            a= collection_1.find({"sku":i["sku"]})
            # se busca datos en offer1 cada iteracion
            a=list(a)
        
            b= collection_2.find({"sku":i["sku"]})
            # se busca datos en offer2  en cada iteracion 
            b = list(b)
            #print(b)
            len_b = len(b)
            print(len_b)

            if len_b == 0:
                print(" NO EXSTE EN BASE DE DATOS ")
                save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                            i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],ship_db2)
                if  i["card_price"] == 0:
                        card_price = ""
                else:
                    card_price = '\n👉Precio Tarjeta :'+str(i["card_price"])

                if i["list_price"] == 0:
                   list_price = ""
                else:
                        list_price = '\n\n➡️Precio Lista :'+str(i["list_price"])

                if i["web_dsct"] <= 50:
                    dsct = "🟡"
                if i["web_dsct"] > 50 and i["web_dsct"]  <=69:
                    dsct = "🟢"
                if i["web_dsct"] >=70:
                    dsct = "🔥🔥🔥🔥🔥🔥"

                # try:
                #     historic = minimo(i["sku"])[3]
                # except:
                #     historic = False
                # print(historic)

                # if historic == True:

                #     historic_min = "\n🔥🔥🔥🔥🔥🔥🔥 Minimo historico"
                #     historic_list = "\nPrecio minimo: "+str(minimo(i["sku"])[0])+"\n"+"Precio anterior: "+str(minimo(i["sku"])[1])+"\n"+"Precio maximo: "+str(minimo(i["sku"])[2])
                # if historic == False:

                historic_min = ""
                historic_list=""

                msn =  "✅Marca: "+str(i["brand"])+"\n✅"+str(i["product"])+list_price+"\n👉Precio web :"+str(i["best_price"])+card_price+"\n"+dsct+"Descuento: "+"% "+str(i["web_dsct"])+"\n"+"\n\n⌛"+i["date"]+" "+ i["time"]+"\n🔗Link :"+str(i["link"])+"\n🏠home web:"+i["home_list"]+"\n\n◀️◀️◀️◀️◀️◀️◀️▶️▶️▶️▶️▶️▶️"

        
                foto = i["image"]

                print(len(foto))

                if len(foto) <5:
                    print(len(foto))
                    foto="https://westsiderc.org/wp-content/uploads/2019/08/Image-Not-Available.png"
                
              
                try:
                    send_telegram (msn, foto, bot_token, chat_id)
                    time.sleep(1)
                except:
                    continue
           
                print(" PRODUCTO EN BASE B NO EXISTE, SE ENVIA A TELEGRAM")
                continue


            if b!=a:
                #send_telegram( ("<b>Marca: "+i["brand"]+"</b>\nModelo: "+i["product"]+"\nPrecio Lista :" +str(i["list_price"])+ "\n<b>Precio web :"+str(i["best_price"])+"</b>\nPrecio Tarjeta :"+str(i["card_price"])+"\n"+i["image"]+"\nLink :"+str(i["link"])))
                print("PRODUCTO DE A ES DIFERENTE DE B,  SE ENVIA  A TELEGRAM")
               
                save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                            i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],ship_db2)
                continue
            if a==b:
                print("SON IGUALES,  NO SE ENVIA TELEGRAM")

    gc.collect()


##############################################################################################################

def auto_telegram_between_values_custom_bd( ship_db1,ship_db2, bot_token, chat_id,porcentage1, 
                                           porcentage2, producto,db_name,db_collection):
    print("se esta ejecutando")
    product_array = []

    db = client[db_name]
    collection = db[db_collection]
    db.command({"planCacheClear": "scrap"})

    t1 =  collection.find( {"web_dsct":{ "$gte":porcentage1, "$not":{"$gte":porcentage2}},"date":date , "product":{"$not":{"$in":[re.compile(producto,re.IGNORECASE),re.compile("reloj",re.IGNORECASE) ]} } })

    collection_1 = db[ship_db1]
    collection_2 = db[ship_db2]

    
    for i in t1:
        product_array.append(i)

    
    for i in product_array:
            save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                           i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],ship_db1)
            f = print("se graba en bd datos")

    
            a= collection_1.find({"sku":i["sku"]})
            # se busca datos en offer1 cada iteracion
            a=list(a)
            print(a)
            
        
            b= collection_2.find({"sku":i["sku"]})
            # se busca datos en offer2  en cada iteracion 
            b = list(b)
            print(b)
            len_b = len(b)
            print(len_b)


            if len_b == 0:
                print(" no exitse en base de daos 2, se graba")
                save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                            i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],ship_db2)
                print("SE GRABO EN BASE DE DATOS 2")

                if  i["card_price"] == 0:
                    card_price = ""
                else:
                    card_price = '\n👉Precio Tarjeta :'+str(i["card_price"])

                if i["list_price"] == 0:
                     list_price = ""
                else:
                    list_price = '\n\n➡️Precio Lista :'+str(i["list_price"])

                if i["web_dsct"] <= 50:
                    dsct = "🟡"
                if i["web_dsct"] > 50 and i["web_dsct"]  <=69:
                    dsct = "🟢"
                if i["web_dsct"] >=70:
                    dsct = "🔥🔥🔥🔥🔥🔥"

                # try:
                #     historic = minimo(i["sku"])[3]
                # except:
                #     historic = False
                # print(historic)

                # if historic == True:

                #     historic_min = "\n🔥🔥🔥🔥🔥🔥🔥 Minimo historico"
                #     historic_list = "\nPrecio minimo: "+str(minimo(i["sku"])[0])+"\n"+"Precio anterior: "+str(minimo(i["sku"])[1])+"\n"+"Precio maximo: "+str(minimo(i["sku"])[2])
                # if historic == False:

                historic_min = ""
                historic_list=""

                msn =  "✅Marca: "+str(i["brand"])+"\n✅"+str(i["product"])+list_price+"\n👉Precio web :"+str(i["best_price"])+card_price+"\n"+dsct+"Descuento: "+"% "+str(i["web_dsct"])+"\n"+"\n\n⌛"+i["date"]+" "+ i["time"]+"\n🔗Link :"+str(i["link"])+"\n🏠home web:"+i["home_list"]+"\n\n◀️◀️◀️◀️◀️◀️◀️▶️▶️▶️▶️▶️▶️"


                foto = i["image"]
                print("#########")
                print(foto)
                print("#########")
                print(len(foto))

                if len(foto) <5 :
                    print(len(foto))
                    foto="https://westsiderc.org/wp-content/uploads/2019/08/Image-Not-Available.png"
                
                if not foto:
                    foto="https://westsiderc.org/wp-content/uploads/2019/08/Image-Not-Available.png"
                


            
                try:
                    send_telegram (msn, foto, bot_token, chat_id)
                    time.sleep(1) 
                except: continue
                # send_telegram( ("<b>Marca: "+i["brand"]+"</b>\nModelo: "+i["product"]+"\nPrecio Lista :" +str(i["list_price"])+ "\n<b>Precio web :"+str(i["best_price"])+"</b>\nPrecio Tarjeta :"+str(i["card_price"])+"\n"+"Descuento: "+"%"+str(i["web_dsct"])+"\n"+i["date"]+" "+ i["time"]+"\n"+i["image"]+"\nLink :"+str(i["link"])+"\nhome web:"+i["home_list"])
                #                 ,bot_token, chat_id)
                

                print(" PRODUCTO EN BASE B NO EXISTE, SE ENVIA A TELEGRAM")
                continue


            if b!=a:
                #send_telegram( ("<b>Marca: "+i["brand"]+"</b>\nModelo: "+i["product"]+"\nPrecio Lista :" +str(i["list_price"])+ "\n<b>Precio web :"+str(i["best_price"])+"</b>\nPrecio Tarjeta :"+str(i["card_price"])+"\n"+i["image"]+"\nLink :"+str(i["link"])))
                print("PRODUCTO DE A ES DIFERENTE DE B,  SE ENVIA  A TELEGRAM")
               
                save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                            i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],ship_db2)
                continue
            if a==b:
                print("SON IGUALES,  NO SE ENVIA TELEGRAM")

    gc.collect()

##################################################################################################
##################################################################################################
def manual_telegram( category, dsct, bot_token, chat_id):
    
    db = client["brands"]
    collection= db[category]
    
    t9 = collection.find({})

    array_brand= []

    for i in t9:
        array_brand.append(i["brand"])
        
    print(array_brand)
   # for brand in array_brand:
     
    db = client["scrap"]
    collection = db["scrap"]
    db.command({"planCacheClear": "scrap"})

    
# t1 =  collection.find( {"web_dsct":{ "$gte":int(dsct)},"date":date ,"brand":{"$in":[ re.compile(brand,re.IGNORECASE) ]}})
   
    #db.command({"planCacheClear": "scrap"})
    t1 =  collection.find( {"web_dsct":{ "$gte":int(dsct)},"date":date ,"brand":{"$in":[ re.compile(brand,re.IGNORECASE) for brand in array_brand ] }})
    print(t1)
    print("pasa por aqui")
    for i in t1:
        print(i)
     
    
        send_telegram( ("<b>Marca: "+i["brand"]+"</b>\nModelo: "+i["product"]+"\nPrecio Lista :" +str(i["list_price"])+ "\n<b>Precio web :"+str(i["best_price"])+"</b>\nPrecio Tarjeta :"+str(i["card_price"])+"\n"+"Descuento: "+"%"+str(i["web_dsct"])+"\n"+i["date"]+" "+ i["time"]+"\n"+i["image"]+"\nLink :"+str(i["link"])),
                       bot_token, chat_id)
        time.sleep(1)
    gc.collect()
    
             

def search_market2_dsct(market,dsct,price, bot_token, chat_id ):
    db5.command({"planCacheClear": "scrap"})
    
    if price == None:

        if market == "all":
                t5 = collection5.find({ "web_dsct":{"$gte":int(dsct)}, "brand":{"$nin":[re.compile("generica", re.IGNORECASE), re.compile("generico", re.IGNORECASE),  re.compile("genérico", re.IGNORECASE), re.compile("genérica", re.IGNORECASE),  re.compile("generic", re.IGNORECASE)] }, "date": date}).sort("web_dsct",pymongo.DESCENDING)
        else:
            
         t5 = collection5.find({"market":market, "web_dsct":{"$gte":int(dsct)}, "brand":{"$nin":[re.compile("generica", re.IGNORECASE), re.compile("generico", re.IGNORECASE),  re.compile("genérico", re.IGNORECASE), re.compile("genérica", re.IGNORECASE),  re.compile("generic", re.IGNORECASE)] }, "date": date}).sort("web_dsct",pymongo.DESCENDING)

    if price == "+":
    
        if market == "all":
                t5 = collection5.find({ "web_dsct":{"$gte":int(dsct)}, "brand":{"$nin":[re.compile("generica", re.IGNORECASE), re.compile("generico", re.IGNORECASE),  re.compile("genérico", re.IGNORECASE), re.compile("genérica", re.IGNORECASE),  re.compile("generic", re.IGNORECASE)] }, "date": date}).sort("best_price",pymongo.DESCENDING)
        else:
            
         t5 = collection5.find({"market":market, "web_dsct":{"$gte":int(dsct)}, "brand":{"$nin":[re.compile("generica", re.IGNORECASE), re.compile("generico", re.IGNORECASE),  re.compile("genérico", re.IGNORECASE), re.compile("genérica", re.IGNORECASE),  re.compile("generic", re.IGNORECASE)] }, "date": date}).sort("best_price",pymongo.DESCENDING)

    if price == "-":
    
        if market == "all":
                t5 = collection5.find({ "web_dsct":{"$gte":int(dsct)}, "brand":{"$nin":[re.compile("generica", re.IGNORECASE), re.compile("generico", re.IGNORECASE),  re.compile("genérico", re.IGNORECASE), re.compile("genérica", re.IGNORECASE),  re.compile("generic", re.IGNORECASE)] }, "date": date}).sort("best_price",pymongo.ASCENDING)
        else:
            
         t5 = collection5.find({"market":market, "web_dsct":{"$gte":int(dsct)}, "brand":{"$nin":[re.compile("generica", re.IGNORECASE), re.compile("generico", re.IGNORECASE),  re.compile("genérico", re.IGNORECASE), re.compile("genérica", re.IGNORECASE),  re.compile("generic", re.IGNORECASE)] }, "date": date}).sort("best_price",pymongo.ASCENDING)

    if dsct == 0:
         t5 = collection5.find({"market":market, "brand":{"$nin":[re.compile("generica", re.IGNORECASE), re.compile("generico", re.IGNORECASE),  re.compile("genérico", re.IGNORECASE), re.compile("genérica", re.IGNORECASE),  re.compile("generic", re.IGNORECASE)] }, "date": date}).sort("web_dsct",pymongo.DESCENDING)
    if dsct == 0 and price == "+":
        t5 = collection5.find({"market":market,  "brand":{"$nin":[re.compile("generica", re.IGNORECASE), re.compile("generico", re.IGNORECASE),  re.compile("genérico", re.IGNORECASE), re.compile("genérica", re.IGNORECASE),  re.compile("generic", re.IGNORECASE)] }, "date": date}).sort("best_price",pymongo.DESCENDING)
    if dsct == 0 and price == "-":
        t5 = collection5.find({"market":market,  "brand":{"$nin":[re.compile("generica", re.IGNORECASE), re.compile("generico", re.IGNORECASE),  re.compile("genérico", re.IGNORECASE), re.compile("genérica", re.IGNORECASE),  re.compile("generic", re.IGNORECASE)] }, "date": date}).sort("best_price",pymongo.ASCENDING)

    list_cur = list(t5)
    products = []
    for i in list_cur:
        p = {"market": i["market"],"brand": i["brand"], "product": i["product"], 'list_price': i["list_price"], 'best_price': i["best_price"], 'card_price': i["card_price"], 'web_dsct': "%"+str(i["web_dsct"]), 'card_dsct': i["card_dsct"], 'link':  '<a href='+i["link"]+'>Link</a>' , 'image': '<img src='+str(i["image"])+" style=max-height:124px;/>", 'date': i["date"], 'time':i["time"], "sku":str(i["sku"])}
        products.append(p)

    df = DataFrame(products)
    
    def path_to_image_html(path):
 
        return '<img src="'+ path + '" style=max-height:124px;"/>'

    html = df.to_html(escape=False ,formatters=dict(column_name_with_image_links=path_to_image_html))

    with open (config("HTML_PATH")+market+".html", "w", encoding='utf-8') as f:
     
        f.write(html)
        f.close
    print(html)

    #send_telegram(html, bot_token, chat_id )
    #print("se envia html")
    #gc.collect()


# SE BUSCA POR PRODUCTO 
def search_product_dsct_html(product,dsct, price, bot_token, chat_id):
    db5.command({"planCacheClear": "scrap"})
    product = str(product).replace("%"," ")
    print(price)
    if price == "+":
        t5 = collection5.find({"product":{"$in":[re.compile(product, re.IGNORECASE),]}, "web_dsct":{"$gte":int(dsct)}, "brand":{"$nin":[re.compile("generica", re.IGNORECASE), re.compile("generico", re.IGNORECASE),  re.compile("genérico", re.IGNORECASE), re.compile("genérica", re.IGNORECASE),  re.compile("generic", re.IGNORECASE)] }, "date": date}).sort("best_price",pymongo.DESCENDING)
    if price =="-":
        t5 = collection5.find({"product":{"$in":[re.compile(product, re.IGNORECASE),]}, "web_dsct":{"$gte":int(dsct)}, "brand":{"$nin":[re.compile("generica", re.IGNORECASE), re.compile("generico", re.IGNORECASE),  re.compile("genérico", re.IGNORECASE), re.compile("genérica", re.IGNORECASE),  re.compile("generic", re.IGNORECASE)] }, "date": date}).sort("best_price",pymongo.ASCENDING)

    if price ==None:
       t5 = collection5.find({"product":{"$in":[re.compile(product, re.IGNORECASE),]}, "web_dsct":{"$gte":int(dsct)}, "brand":{"$nin":[re.compile("generica", re.IGNORECASE), re.compile("generico", re.IGNORECASE),  re.compile("genérico", re.IGNORECASE), re.compile("genérica", re.IGNORECASE),  re.compile("generic", re.IGNORECASE)] }, "date": date}).sort("web_dsct",pymongo.DESCENDING)

    if dsct == 0:
        t5 = collection5.find({"product":{"$in":[re.compile(product, re.IGNORECASE),]},  "brand":{"$nin":[re.compile("generica", re.IGNORECASE), re.compile("generico", re.IGNORECASE),  re.compile("genérico", re.IGNORECASE), re.compile("genérica", re.IGNORECASE),  re.compile("generic", re.IGNORECASE)] }, "date": date}).sort("web_dsct",pymongo.ASCENDING)

    if dsct == 0 and price == "+":
        t5 = collection5.find({"product":{"$in":[re.compile(product, re.IGNORECASE),]},  "brand":{"$nin":[re.compile("generica", re.IGNORECASE), re.compile("generico", re.IGNORECASE),  re.compile("genérico", re.IGNORECASE), re.compile("genérica", re.IGNORECASE),  re.compile("generic", re.IGNORECASE)] }, "date": date}).sort("best_price",pymongo.DESCENDING)

    if dsct == 0 and price == "-":
        t5 = collection5.find({"product":{"$in":[re.compile(product, re.IGNORECASE),]},  "brand":{"$nin":[re.compile("generica", re.IGNORECASE), re.compile("generico", re.IGNORECASE),  re.compile("genérico", re.IGNORECASE), re.compile("genérica", re.IGNORECASE),  re.compile("generic", re.IGNORECASE)] }, "date": date}).sort("best_price",pymongo.ASCENDING)



    list_cur = list(t5)
    products = []
    for i in list_cur:
        
        
        
        #p = {"market": i["market"],"brand": i["brand"], "product": i["product"], 'list_price': i["list_price"], 'best_price': i["best_price"], 'card_price': i["card_price"], 'web_dsct': "%"+str(i["web_dsct"]), 'card_dsct': i["card_dsct"], 'link':  '<a href='+i["link"]+'>Link</a>' , 'image': '<img src='+i["image"]+" style=max-height:124px;/>", 'date': i["date"], 'time':i["time"], "sku":i["sku"]}

        p = {"market": i["market"],"brand": i["brand"], "product": i["product"], 'list_price': i["list_price"], 'best_price': i["best_price"], 'card_price': i["card_price"], 'web_dsct': i["web_dsct"],  'link':  '<a href='+i["link"]+'>Link</a>' , 'image': '<img src='+i["image"]+" style=max-height:124px;/>", 'date': i["date"], 'time':i["time"], "sku":i["sku"]}
        products.append(p)

    df = DataFrame(products)
    
    def path_to_image_html(path):
 
        return '<img src="'+ path + '" style=max-height:124px;"/>'

    html = df.to_html(escape=False ,formatters=dict(column_name_with_image_links=path_to_image_html))

    with open (config("HTML_PATH")+"producto.html", "w", encoding="utf-8") as f:
        f.write(html)
        f.close
    #print(html)
    # send_telegram(html, bot_token, chat_id )
    # os.remove(config("HTML_PATH")+"producto.html")
    gc.collect()

def test2(codigo,bot_token, chat_id):
    db5.command({"planCacheClear": "scrap"})
      
    t5 = collection5.find({"sku":str(codigo)})
    print( "se realizo busqueda")
    print(codigo)
    for i in t5:
        print(i)
        print("se envio a telegram")      
        send_telegram ("<b>Marca: "+i["brand"]+"</b>\nModelo: "+i["product"]+"\nPrecio Lista :"+str(i["list_price"])+"\n<b>Precio web :"+str(i["best_price"])+"</b>\nPrecio Tarjeta :"+str(i["card_price"])+"\n"+"Descuento: "+"%"+str(i["web_dsct"])+"\n"+i["date"]+" "+ i["time"]+"\n"+i["image"]+"\n\nLink :"+i["link"]+"\nhome web:"+i["home_list"],
                       bot_token, chat_id)
    gc.collect()
      



def search_brand_dsct_html(brand,dsct, price, bot_token, chat_id):
    # db5.command({"planCacheClear": "scrap"})
    brand = str(brand).replace("%"," ")
    print(price)
    if price == "+":
        t5 = collection5.find({"brand":{"$in":[re.compile(brand, re.IGNORECASE),]}, "web_dsct":{"$gte":int(dsct)}, "date": date}).sort("best_price",pymongo.DESCENDING)
    if price =="-":
        t5 = collection5.find({"brand":{"$in":[re.compile(brand, re.IGNORECASE),]}, "web_dsct":{"$gte":int(dsct)},"date": date}).sort("best_price",pymongo.ASCENDING)

    if price ==None:
       t5 = collection5.find({"brand":{"$in":[re.compile(brand, re.IGNORECASE),]}, "web_dsct":{"$gte":int(dsct)}, "date": date}).sort("web_dsct",pymongo.DESCENDING)
  
    if dsct == 0:
        t5 = collection5.find({"brand":{"$in":[re.compile(brand, re.IGNORECASE),]},"web_dsct":{"$gte":int(dsct)}, "date": date}).sort("web_dsct",pymongo.ASCENDING)
    if dsct == 0 and price == "+":
        t5 = collection5.find({"brand":{"$in":[re.compile(brand, re.IGNORECASE),]},"web_dsct":{"$gte":int(dsct)},"date": date}).sort("best_price",pymongo.DESCENDING)
    if dsct == 0 and price == "-":
        t5 = collection5.find({"brand":{"$in":[re.compile(brand, re.IGNORECASE),]},"web_dsct":{"$gte":int(dsct)}, "date": date}).sort("best_price",pymongo.ASCENDING)

    
    list_cur = list(t5)
    brands = []
    for i in list_cur:
        p = {"market": i["market"], "brand": i["brand"], "product": i["product"], 'list_price': i["list_price"],
            'best_price': i["best_price"], 'card_price': i["card_price"], 'web_dsct': i["web_dsct"],
            'card_dsct': i["card_dsct"], 'link': '<a href='+i["link"]+'>Link</a>',
            'image': '<img src='+i["image"]+" style=max-height:124px;/>", 'date': i["date"], 'time': i["time"],
            "sku": i["sku"]}
        brands.append(p)
    print(brands)

    df = DataFrame(brands)

    print(df)
    def path_to_image_html(path):
 
        return '<img src="'+ path + '" style=max-height:124px;"/>'

    html = df.to_html(escape=False ,formatters=dict(column_name_with_image_links=path_to_image_html))

    with open (config("HTML_PATH")+brand+".html", "w", encoding="utf-8") as f:
        f.write(html)
        f.close
    #print(html)
    # send_telegram(html, bot_token, chat_id )
    # os.remove(config("HTML_PATH")+"producto.html")
    gc.collect()

    # list_cur = list(t5)
    # brands= []
    # for i in list_cur:
        
       
    #     p = {"market": i["market"],"brand": i["brand"], "product": i["product"], 'list_price': i["list_price"], 'best_price': i["best_price"], 'card_price': i["card_price"], 'web_dsct': i["web_dsct"], 'card_dsct': i["card_dsct"], 'link':  '<a href='+i["link"]+'>Link</a>' , 'image': '<img src='+i["image"]+" style=max-height:124px;/>", 'date': i["date"], 'time':i["time"], "sku":i["sku"]}
    #     brands.append(p)

    # df = DataFrame(brands)
    
    # def path_to_image_html(path):
 
    #     return '<img src="'+ path + '" style=max-height:124px;"/>'

    # html = df.to_html(escape=False ,formatters=dict(column_name_with_image_links=path_to_image_html))

    # with open (config("HTML_PATH")+brand+".html", "w", encoding="utf-8") as f:
    #     f.write(html)
    #     f.close
    # #print(html)
    # # send_telegram(html, bot_token, chat_id )
    # # os.remove(config("HTML_PATH")+"producto.html")
    # gc.collect()


def search_price(market,price_minimo,price_maximo, bot_token ,chat_id):

    db5.command({"planCacheClear": "scrap"})

    t5 = collection5.find({ "date":date ,"market":market, "best_price":{"$gte":int(price_minimo), "$lte":int(price_maximo) }}) 
    

    list_cur = list(t5)
    products = []
    for i in list_cur:
        p = {"market": i["market"],"brand": i["brand"], "product": i["product"], 'list_price': i["list_price"], 'best_price': i["best_price"], 'card_price': i["card_price"], 'web_dsct': "%"+str(i["web_dsct"]), 'card_dsct': i["card_dsct"], 'link':  '<a href='+i["link"]+'>Link</a>' , 'image': '<img src='+str(i["image"])+" style=max-height:124px;/>", 'date': i["date"], 'time':i["time"], "sku":str(i["sku"])}
        products.append(p)

    df = DataFrame(products)
    
    def path_to_image_html(path):
 
        return '<img src="'+ path + '" style=max-height:124px;"/>'

    html = df.to_html(escape=False ,formatters=dict(column_name_with_image_links=path_to_image_html))

    with open (config("HTML_PATH")+market+".html", "w", encoding='utf-8') as f:
     
        f.write(html)
        f.close
    print(html)

    


try:      
    argument = sys.argv[1] 
except: argument = "nope"


if argument == "discovery":

    auto_telegram( "tecno_celular", "scrap", "discoverya","discoveryb", config("CAPITAN_SPOK_TOKEN"), config("DISCOVERY_CHAT_TOKEN"))

if argument == "enterprise":
        auto_telegram( "electro_herramientas_colchones", "scrap", "enterprisea","enterpriseb", config("ENTERPRISE_TOKEN"), config("ENTERPRISE_CHAT_TOKEN"))

if argument == "voyager":
        auto_telegram( "juguetes_bicicleta_abarrates", "scrap", "voyagera","voyagerb", config("CAPITAN_JANEWAY_TOKEN"), config("VOYAGER_CHAT_TOKEN"))
    
if argument == "excelsior":
        auto_telegram( "ropa", "scrap", "excelsiora","excelsiorb", config("CAPITAN_PIKE_TOKEN"),config("EXCELSIOR_CHAT_TOKEN"))



# chat_id = config("DISCOVERY_CHAT_TOKEN")
# bot_token = config("CAPITAN_SPOK_TOKEN")
# search_brand_dsct("WESDAR", 50, bot_token, chat_id)