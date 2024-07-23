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
from history_price import compare_prices

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
    print("se envio mensaje por funcion de telegram")

def send_document(document,bot_token, chat_id):
    # Create a bot instance using your bot token
    bot = telegram.Bot(token=bot_token)

    # Send a document to the chat with ID `chat_id`
    bot.send_document(chat_id=chat_id, document=open(document, 'rb'))

########################################################################
########################################################################
########################################################################

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
    client = MongoClient(config("MONGO_DB"))
     
    def html_creator (array):

        products = []
        for i in array:
    
            p = {"market": i["market"],"brand": i["brand"], "product": i["product"], 'list_price': i["list_price"], 'best_price': i["best_price"], 'card_price': i["card_price"], 'web_dsct': "%"+str(i["web_dsct"]), 'card_dsct': "%"+str(i["card_dsct"]), 'link':  '<a href='+i["link"]+'>Link</a>' , 'image': '<img src='+str(i["image"])+" style=max-height:124px;/>", 'date': i["date"], 'time':i["time"], "sku":str(i["sku"])}

            products.append(p)

        df = DataFrame(products)

        
        def path_to_image_html(path):
    
            return '<img src="'+ path + '" style=max-height:124px;"/>'
        
        html = df.to_html(escape=False ,formatters=dict(column_name_with_image_links=path_to_image_html))

        with open (config("HTML_PATH")+brand+".html", "w", encoding='utf-8') as f:
        
            f.write(html)
            f.close
        print(html)


    query = {"sku": {"$regex": re.compile(codigo, re.IGNORECASE)},
           
            "date": date
            }

    shop = ["saga", "shopstar", "ripley", "coolbox", "wong", "metro", "tailoy", "promart", "oechsle", "hiraoka", "curacao", "platanitos"]

    array =[]
    for i in shop:
        db5 = client[i]
        collection5 = db5["scrap"] 
        html_view = collection5.find(query).sort("web_dsct", -1)
        array.extend(html_view)
    #db5.command({"planCacheClear": "scrap"})

    print( "se realizo busqueda")
    print(codigo)
    for i in array:
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
    
        msn = (
                        "✅Marca: " + str(i["brand"]) + "\n" +
                        "✅" + str(i["product"]) + list_price + "\n" +
                        "👉Precio web: " + str(i["best_price"]) + card_price + "\n" +
                        "🏷Descuento: %" + str(i["web_dsct"]) + " "+dsct+"\n\n" +
                        "🕗" + i["date"] + " " + i["time"] + "\n" +
                        "🌐Link: " + str(i["link"]) + "\n" +
                        "🏠home web: " + i["home_list"] + "\n\n" +
                        "◀️◀️◀️◀️◀️◀️◀️▶️▶️▶️▶️▶️▶️"
                    )
        #msn =  "✅Marca: "+str(i["brand"])+"\n✅"+str(i["product"])+list_price+"\n👉Precio web :"+str(i["best_price"])+card_price+"\n"+dsct+"Descuento: "+"% "+str(i["web_dsct"])+"\n"+"\n\n⌛"+i["date"]+" "+ i["time"]+"\n🔗Link :"+str(i["link"])+"\n🏠home web:"+i["home_list"]+"\n\n◀️◀️◀️◀️◀️◀️◀️▶️▶️▶️▶️▶️▶️"
        
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
   
        msn = (
                        "✅Marca: " + str(i["brand"]) + "\n" +
                        "✅" + str(i["product"]) + list_price + "\n" +
                        "👉**Precio web:** " + "**"+str(i["best_price"])+"**" + card_price + "\n" +
                        "🏷Descuento: %" + str(i["web_dsct"]) + " "+dsct+"\n\n" +
                        "🕗" + i["date"] + " " + i["time"] + "\n" +
                        "🌐Link: " + str(i["link"]) + "\n" +
                        "🏠home web: " + i["home_list"] + "\n\n" +
                        "◀️◀️◀️◀️◀️◀️◀️▶️▶️▶️▶️▶️▶️"
                    )
        #msn =  "✅Marca: "+str(i["brand"])+"\n✅"+str(i["product"])+list_price+"\n👉Precio web :"+str(i["best_price"])+card_price+"\n"+dsct+"Descuento: "+"% "+str(i["web_dsct"])+"\n"+"\n\n⌛"+i["date"]+" "+ i["time"]+"\n🔗Link :"+str(i["link"])+"\n🏠home web:"+i["home_list"]+"\n\n◀️◀️◀️◀️◀️◀️◀️▶️▶️▶️▶️▶️▶️"
        
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
        msn = (
                        "✅Marca: " + str(i["brand"]) + "\n" +
                        "✅" + str(i["product"]) + list_price + "\n" +
                        "👉Precio web: " + str(i["best_price"]) + card_price + "\n" +
                        "🏷Descuento: %" + str(i["web_dsct"]) + " "+dsct+"\n\n" +
                        "🕗" + i["date"] + " " + i["time"] + "\n" +
                        "🌐Link: " + str(i["link"]) + "\n" +
                        "🏠home web: " + i["home_list"] + "\n\n" +
                        "◀️◀️◀️◀️◀️◀️◀️▶️▶️▶️▶️▶️▶️"
                    )
        #msn =  "✅Marca: "+str(i["brand"])+"\n✅"+str(i["product"])+list_price+"\n👉Precio web :"+str(i["best_price"])+card_price+"\n"+dsct+"Descuento: "+"% "+str(i["web_dsct"])+"\n"+"\n\n⌛"+i["date"]+" "+ i["time"]+"\n🔗Link :"+str(i["link"])+"\n🏠home web:"+i["home_list"]+"\n\n◀️◀️◀️◀️◀️◀️◀️▶️▶️▶️▶️▶️▶️"

        
        foto = i["image"]
      
        send_telegram (msn, foto, bot_token, chat_id)
        time.sleep(1)
        print("Se envio mensaje a telegram")
    gc.collect()





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


    t1 =  collection.find( {"web_dsct":{ "$gte":porcentage},"date":date ,"brand":{"$in":array_brand}, "product":{"$nin":array_trash}})
    t2 =  collection.find( {"best_price":{ "$gt": 0, "$lt": 200 },"date":date ,"brand":{"$in":array_brand}, "product":{"$nin":array_trash}})

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
                
    
                msn = (
                  
                        "✅Marca: " + str(i["brand"]) + "\n" +
                        "✅" + str(i["product"]) + list_price + "\n" +
                        "👉Precio web: " + str(i["best_price"]) + card_price + "\n" +
                        "🏷Descuento: %" + str(i["web_dsct"]) + " "+dsct+"\n\n" +
                        "🕗" + i["date"] + " " + i["time"] + "\n" +
                        "🌐Link: " + str(i["link"]) + "\n" +
                        "🏠home web: " + i["home_list"] + "\n\n" +
                        "◀️◀️◀️◀️◀️◀️◀️▶️▶️▶️▶️▶️▶️"#############################
                    )

                # msn =  "✅Marca: "+str(i["brand"])+"\n✅"+str(i["product"])+list_price+"\n👉Precio web :"+str(i["best_price"])+card_price+"\n"+dsct+"Descuento: "+"% "+str(i["web_dsct"])+"\n"+"\n\n⌛"+i["date"]+" "+ i["time"]+"\n🔗Link :"+str(i["link"])+"\n🏠home web:"+i["home_list"]+"\n\n◀️◀️◀️◀️◀️◀️◀️▶️▶️▶️▶️▶️▶️"
                foto = i["image"]
                send_telegram(msn, foto, bot_token, chat_id)
                print(chat_id)
                print(bot_token)
                print(" PRODUCTO EN BASE B NO EXISTE, SE ENVIA A TELEGRAM")
                


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

    print(product_array)
    

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
##################################################################################################
def auto_telegram_between_values(  ship_db1,ship_db2, bot_token, chat_id,porcentage1, porcentage2, producto, bd_name, collection_name):
    print("buscando")
   
    db = client[bd_name]
    collection = db[collection_name]
    collection_1 = db[ship_db1]

    ##########  OBTENGO LAS LISTAS DEL MONGO DE LOS PRODUCTOS CON EL RANGO DE DESCUENTO ##########
    live_search = collection.find({
        "$or": [
            {"web_dsct": {"$gte": porcentage1, "$lte": porcentage2}},
            {"card_dsct": {"$gte": porcentage1,  "$lte": porcentage2}},
        ],
        "date": date,
        "product": {"$not": {"$in": [re.compile(producto, re.IGNORECASE), re.compile("reloj", re.IGNORECASE)]}}
            })
    #==================================================================================
    print("obtiene data de base principal")
    product_array = []
    count = 0
    for i in live_search:
        count +=1

        data_live ={
               "sku": i["sku"],
                "best_price":i["best_price"],
                "list_price":i["list_price"],
                "card_price":i["card_price"],
                "web_dsct":i["web_dsct"],
               "card_dsct": i["card_dsct"],    
            }
        
        try:
            data_saved = collection_1.find_one({'sku': i['sku']})
        
            data_sv = {
                "sku": data_saved["sku"],
                "best_price":data_saved["best_price"],
                "list_price":data_saved["list_price"],
                "card_price":data_saved["card_price"],
                "web_dsct":data_saved["web_dsct"],
                "card_dsct": data_saved["card_dsct"],
            }
        except:
            data_sv = None
        print("######################################################################")
        print("ESTO ES DATA DE LA BASE DE DATOS TIEMPO REAL")
        print(data_live)
        print()
        print(count)
        print()
        print(" BASE DE DATOS DE COMPARACION")
        print(data_sv)
        print()
        print("######################################################################")

   
        if data_live == data_sv:

            print("PRODUCTOS IGUALES, NO SE MANDA NADA A TELEGRAM Y NO DEBE GRABARSE TAMPOCO")
        
        if data_live != data_sv:
           

            if i["web_dsct"] <= 50:
                web_d = "🟡"
            if i["web_dsct"]  > 50 and i["web_dsct"]  <=69:
                web_d = "🟢"
            if i["web_dsct"]  >=70:
                web_d = "🔥🔥🔥🔥🔥🔥🔥"

            if i["card_dsct"] <= 50:
                card_d = "🟡"
            if i["card_dsct"] > 50 and i["card_dsct"]  <=69:
                card_d = "🟢"
            if i["card_dsct"]  >=70:
                card_d = "🔥🔥🔥🔥🔥🔥🔥"

            
            if i["list_price"] == 0:
                list_price = ""
            else:
                list_price = '🏷 <b>Precio lista:</b> '+  str(i["list_price"])+"\n" 
            
            if i["best_price"] == 0:
                best_price = ""
            else:
                best_price = '👉 <b>Precio web:</b> <b>'+ str(i["best_price"]) + "</b>" +"\n" 

            if i["card_price"] == 0:
                card_price = ""
            else:
                card_price = '💳 <b>Precio TC:</b> <b>' +str(i["card_price"])+ "</b>"+"\n" 

            if i["card_dsct"] == 0:
                card_dsct = ""
            else:
                card_dsct =  "💥 <b>Descuento TC:</b> %" + str(i["card_dsct"])+ card_d+"\n" 

            if i["web_dsct"] == 0:
                web_dsct = ""
            else:
                web_dsct =   "💵 <b>Descuento web:</b> %" + str(i["web_dsct"])+ web_d+  "\n" 
    
            
            

            msn = (
                
                    "🌟🦙 <b>Detalles del Producto</b> 🦙🌟\n\n" +
                    "✅ <b>Marca:</b> " + str(i["brand"]) + "\n" +
                    "📦 <b>Producto:</b> " + str(i["product"])  + "\n\n" +
                    list_price+
                    best_price +
                    card_price+
                    "\n"+
                    card_dsct+
                    web_dsct+
                    "🏬 <b>Market:</b> " + i["market"] + "\n" +
                    "🕗 <b>Fecha y Hora:</b> " + i["date"] + " " + i["time"] + "\n" +
                    "🔗 <b>Enlace:</b> <a href='" + str(i["link"]) + "'>Link aquí</a>\n\n" 
            )


            foto = i["image"]

            if len(foto) <5:
        
                foto="https://westsiderc.org/wp-content/uploads/2019/08/Image-Not-Available.png"

            save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                        i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"], i["card_dsct"],bd_name,ship_db1)
            
            send_telegram (msn, foto, bot_token, chat_id)

            print(data_live)
            print()
            print(data_sv)
            print()
            print("LOS DATOS DEL PRODUCTO VARIO Y SE ENVIA A TELEGRAM  Y SE GUARDA EN LA BASE DE DTAOS DE COMPARACION")
            print("###################################################################################")
            print("###################################################################################")
            print("###################################################################################")
            print(i["product"])
            print(i["home_list"])


        if data_live == data_sv:

            print(data_live)
            print()
            print(data_sv)
            print()
            print("LOS DATOS DEL PRODUCTO VARIO Y SE ENVIA A TELEGRAM  Y SE GUARDA EN LA BASE DE DTAOS DE COMPARACION")
            print(i["sku"])
          
                
                
        


            
                


        

        
    
#         documento = i
#         collection.update_one(
#                 {'_id': documento['_id']},
#                 {'$set': documento},
#                 upsert=True
#             )




          
#     #  PRODUCTO EXISTE PARA SER COMPARADO 
    
#     for i in product_array:
#             save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
#                           i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"], i["card_dsct"],bd_name,ship_db1)
            

#             if i["web_dsct"] <= 50:
#                 web_d = "🟡"
#             if i["web_dsct"]  > 50 and i["web_dsct"]  <=69:
#                 web_d = "🟢"
#             if i["web_dsct"]  >=70:
#                 web_d = "🔥🔥🔥🔥🔥🔥🔥"

#             if i["card_dsct"] <= 50:
#                 card_d = "🟡"
#             if i["card_dsct"] > 50 and i["card_dsct"]  <=69:
#                 card_d = "🟢"
#             if i["card_dsct"]  >=70:
#                 card_d = "🔥🔥🔥🔥🔥🔥🔥"

            
#             if i["list_price"] == 0:
#                 list_price = ""
#             else:
#                 list_price = '🏷 <b>Precio lista:</b> '+  str(i["list_price"])+"\n" 
            
#             if i["best_price"] == 0:
#                 best_price = ""
#             else:
#                 best_price = '👉 <b>Precio web:</b> <b>'+ str(i["best_price"]) + "</b>" +"\n" 

#             if i["card_price"] == 0:
#                 card_price = ""
#             else:
#                 card_price = '💳 <b>Precio TC:</b> <b>' +str(i["card_price"])+ "</b>"+"\n" 

#             if i["card_dsct"] == 0:
#                 card_dsct = ""
#             else:
#                 card_dsct =  "💥 <b>Descuento TC:</b> %" + str(i["card_dsct"])+ card_d+"\n" 

#             if i["web_dsct"] == 0:
#                 web_dsct = ""
#             else:
#                 web_dsct =   "💵 <b>Descuento web:</b> %" + str(i["web_dsct"])+ web_d+  "\n" 
    
            
            

#             msn = (
                
#                     "🌟🦙 <b>Detalles del Producto</b> 🦙🌟\n\n" +
#                     "✅ <b>Marca:</b> " + str(i["brand"]) + "\n" +
#                     "📦 <b>Producto:</b> " + str(i["product"])  + "\n\n" +
#                     list_price+
#                     best_price +
#                     card_price+
#                     "\n"+
#                     card_dsct+
#                     web_dsct+
#                     "🕗 <b>Fecha y Hora:</b> " + i["date"] + " " + i["time"] + "\n" +
#                     "🔗 <b>Enlace:</b> <a href='" + str(i["link"]) + "'>Link aquí</a>\n\n" 
#             )
           

# # Envía este mensaje_telegram como respuesta en tu código para Telegram

#             foto = i["image"]

#             print(len(foto))


#             if len(foto) <5:
#                 print(len(foto))
#                 foto="https://westsiderc.org/wp-content/uploads/2019/08/Image-Not-Available.png"
            
          
           
            
#             a= collection_1.find({"sku":i["sku"]})
#             # se busca datos en offer1 cada iteracion
#             a=list(a)
#             print("##############    este es el dab A")
#             print("####################################")
#             print(a)
#             print("####################################")
#             print()

          

#             b= collection_2.find({"sku":i["sku"]})
#             # se busca datos en offer2  en cada iteracion 
#             b = list(b)
#             print("##############    este es el dab B")
#             print("####################################")
#             print(a)
#             print("####################################")
#             print()            
#             print()

           
        
#             len_b = len(b)

          
           
#             if len_b == 0:
      
#                 print("No existe array en base de datos 2")
      
                
#                 save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
#                             i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"], i["card_dsct"],bd_name,ship_db2)
                
              
#                 send_telegram (msn, foto, bot_token, chat_id)
            
#             pro_a = []

#             pro_b = []
        
#             for productA in a:
#                 best_priceA = productA["best_price"]
#                 list_priceA = productA["list_price"]
#                 card_priceA = productA["card_price"]
#                 web_dsctA = productA["web_dsct"]
#                 card_dsctA=productA["card_dsct"]
#                 pro_a.append([best_priceA,list_priceA,card_priceA,web_dsctA,card_dsctA])


#             for productB in b:
#                 best_priceB = productB["best_price"]
#                 list_priceB= productB["list_price"]
#                 card_priceB = productB["card_price"]
#                 web_dsctB = productB["web_dsct"]
#                 card_dsctB=productB["card_dsct"]
#                 pro_b.append([best_priceB,list_priceB,card_priceB,web_dsctB,card_dsctB])

                
#             if pro_a!=pro_b:
           

#                 print("PRODUCTO DE A ES DIFERENTE DE B,  SE ENVIA  A TELEGRAM")

#                 send_telegram (msn, foto, bot_token, chat_id)
            
#                 save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
#                             i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],i["card_dsct"],bd_name,ship_db2)
#                 print("son diferentes")
   
          
                
#             if a==b:
#                 print("SON IGUALES,  NO SE ENVIA TELEGRAM")

        



##############################################################################################################
##################################################################################################
##################################################################################################
##################################################################################################

def auto_telegram_between_values_custom_bd( ship_db1,ship_db2, bot_token, chat_id,porcentage1, 
                                           porcentage2, producto,db_name,db_collection):
    print("se esta ejecutando")
    product_array = []

    db = client[db_name]
    collection = db[db_collection]
    
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
            print("arriba se imprimio B")
            time.sleep(15)
            len_b = len(b)
            print(len_b)


            if len_b == 0:

                print(" no exitse en base de daos 2, se graba")
                save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                            i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],ship_db2)
                print("SE GRABO EN BASE DE DATOS 2")
                time.sleep(15)
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


                msn = (
                        "✅Marca: " + str(i["brand"]) + "\n" +
                        "✅" + str(i["product"]) + list_price + "\n" +
                        "👉Precio web: " + str(i["best_price"]) + card_price + "\n" +
                        "🏷Descuento: %" + str(i["web_dsct"]) + " "+dsct+"\n\n" +
                        "🕗" + i["date"] + " " + i["time"] + "\n" +
                        "🌐Link: " + str(i["link"]) + "\n" +
                        "🏠home web: " + i["home_list"] + "\n\n" +
                        "◀️◀️◀️◀️◀️◀️◀️▶️▶️▶️▶️▶️▶️"
                    )


                foto = i["image"]

                if len(foto) <5 :
                    print(len(foto))
                    foto="https://westsiderc.org/wp-content/uploads/2019/08/Image-Not-Available.png"
                
                if not foto:
                    foto="https://westsiderc.org/wp-content/uploads/2019/08/Image-Not-Available.png"
                


                send_telegram (msn, foto, bot_token, chat_id)
                print("SE ENVIA A TELEGRAM")
        
               
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
    
##############################################################################################################################
##############################################################################################################################
##############################################################################################################################
##############################################################################################################################
##############################################################################################################################

def search_market2_dsct(market,dsct,price, bot_token, chat_id ):
    date_local = dia()
    client = MongoClient(config("MONGO_DB"))
    db5 = client[market]
    collection5 = db5["scrap"] 

    def html_creator (array):

        products = []
        for i in array:
    
            p = {"market": i["market"],"brand": i["brand"], "product": i["product"], 'list_price': i["list_price"], 'best_price': i["best_price"], 'card_price': i["card_price"], 'web_dsct': "%"+str(i["web_dsct"]), 'card_dsct': "%"+str(i["card_dsct"]), 'link':  '<a href='+i["link"]+'>Link</a>' , 'image': '<img src='+str(i["image"])+" style=max-height:124px;/>", 'date': i["date"], 'time':i["time"], "sku":str(i["sku"])}

            products.append(p)

        df = DataFrame(products)

        
        def path_to_image_html(path):
    
            return '<img src="'+ path + '" style=max-height:124px;"/>'
        
        html = df.to_html(escape=False ,formatters=dict(column_name_with_image_links=path_to_image_html))

        with open (config("HTML_PATH")+market+".html", "w", encoding='utf-8') as f:
        
            f.write(html)
            f.close
        print(html)


    query = {
            "$or": [
                {"web_dsct": {"$gte": int(dsct)}},
                {"card_dsct": {"$gte": int(dsct)}}
            ],
            "date": date_local
            }
    
  

    shop = ["saga","plazavea", "shopstar", "ripley", "coolbox", "wong", "metro", "tailoy", "promart", "oechsle", "hiraoka", "curacao", "platanitos"]

    if market in shop:
        html_view = collection5.find(query).sort("web_dsct", -1)
        html_view = list(html_view)
        print(html_view)
        html_creator(list(html_view))

    if market == "all": 
        array = []

        for i in shop:
            db5 = client[i]
            collection5 = db5["scrap"] 
            html_view = collection5.find(query).sort("web_dsct", -1)
            array.extend(html_view)

        html_creator(list(array))


            





# SE BUSCA POR PRODUCTO 
def search_product_dsct_html(product,dsct, price, bot_token, chat_id):
    client = MongoClient(config("MONGO_DB"))
     
    def html_creator (array):

        products = []
        for i in array:
    
            p = {"market": i["market"],"brand": i["brand"], "product": i["product"], 'list_price': i["list_price"], 'best_price': i["best_price"], 'card_price': i["card_price"], 'web_dsct': "%"+str(i["web_dsct"]), 'card_dsct': "%"+str(i["card_dsct"]), 'link':  '<a href='+i["link"]+'>Link</a>' , 'image': '<img src='+str(i["image"])+" style=max-height:124px;/>", 'date': i["date"], 'time':i["time"], "sku":str(i["sku"])}

            products.append(p)

        df = DataFrame(products)

        
        def path_to_image_html(path):
    
            return '<img src="'+ path + '" style=max-height:124px;"/>'
        
        html = df.to_html(escape=False ,formatters=dict(column_name_with_image_links=path_to_image_html))

        with open (config("HTML_PATH")+product+".html", "w", encoding='utf-8') as f:
        
            f.write(html)
            f.close
        print(html)


    query = {"product": {"$regex": re.compile(product, re.IGNORECASE)},
            "$or": [
                {"web_dsct": {"$gte": int(dsct)}},
                {"card_dsct": {"$gte": int(dsct)}}
            ],
            "date": date
            }

    shop = ["saga","plazavea", "shopstar", "ripley", "coolbox", "wong", "metro", "tailoy", "promart", "oechsle", "hiraoka", "curacao", "platanitos"]

    array =[]
    for i in shop:
        db5 = client[i]
        collection5 = db5["scrap"] 
        html_view = collection5.find(query).sort("web_dsct", -1)
        array.extend(html_view)

    html_creator(list(array))


def search_brand_dsct_html(brand, dsct, price, bot_token, chat_id):
    client = MongoClient(config("MONGO_DB"))
     
    def html_creator (array):

        products = []
        for i in array:
    
            p = {"market": i["market"],"brand": i["brand"], "product": i["product"], 'list_price': i["list_price"], 'best_price': i["best_price"], 'card_price': i["card_price"], 'web_dsct': "%"+str(i["web_dsct"]), 'card_dsct': "%"+str(i["card_dsct"]), 'link':  '<a href='+i["link"]+'>Link</a>' , 'image': '<img src='+str(i["image"])+" style=max-height:124px;/>", 'date': i["date"], 'time':i["time"], "sku":str(i["sku"])}

            products.append(p)

        df = DataFrame(products)

        
        def path_to_image_html(path):
    
            return '<img src="'+ path + '" style=max-height:124px;"/>'
        
        html = df.to_html(escape=False ,formatters=dict(column_name_with_image_links=path_to_image_html))

        with open (config("HTML_PATH")+brand+".html", "w", encoding='utf-8') as f:
        
            f.write(html)
            f.close
        print(html)


    query = {"brand": {"$regex": re.compile(brand, re.IGNORECASE)},
            "$or": [
                {"web_dsct": {"$gte": int(dsct)}},
                {"card_dsct": {"$gte": int(dsct)}}
            ],
            "date": date
            }

    shop = ["saga", "plazavea", "shopstar", "ripley", "coolbox", "wong", "metro", "tailoy", "promart", "oechsle", "hiraoka", "curacao", "platanitos"]

    array =[]
    for i in shop:
        db5 = client[i]
        collection5 = db5["scrap"] 
        html_view = collection5.find(query).sort("web_dsct", -1)
        array.extend(html_view)

    html_creator(list(array))


def cat_search(category,dsct,bot_token, chat_id):
    print(category)
    print(dsct)

    db = client["brands"]
    collection= db[category]

    t9 = collection.find({})

    array_brand= []

    for i in t9:
        array_brand.append(i["brand"])
    print(array_brand)
    

    db = client["scrap"]
    collection= db["scrap"]

    t1 = collection.find( {"web_dsct":{ "$gte":int(dsct)},"date":date ,"brand":{"$in":[ re.compile(brand,re.IGNORECASE) for brand in array_brand ] }})

    list_cur = list(t1)
    products = []
    for i in list_cur:
        p = {"market": i["market"],"brand": i["brand"], "product": i["product"], 'list_price': i["list_price"], 'best_price': i["best_price"], 'card_price': i["card_price"], 'web_dsct': "%"+str(i["web_dsct"]), 'card_dsct': i["card_dsct"], 'link':  '<a href='+i["link"]+'>Link</a>' , 'image': '<img src='+str(i["image"])+" style=max-height:124px;/>", 'date': i["date"], 'time':i["time"], "sku":str(i["sku"])}

        products.append(p)

    df = DataFrame(products)

    def path_to_image_html(path):
 
        return '<img src="'+ path + '" style=max-height:124px;"/>'

    html = df.to_html(escape=False ,formatters=dict(column_name_with_image_links=path_to_image_html))

    with open (config("HTML_PATH")+category+".html", "w", encoding='utf-8') as f:
     
        f.write(html)
        f.close
    print(html)


def auto_telegram_category( category, ship_db1,ship_db2, bot_token, chat_id,porcentage):
    
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


    t1 =  collection.find( {"web_dsct":{ "$gte":porcentage},"date":date ,"brand":{"$in":array_brand}, "product":{"$nin":array_trash}})
    t2 =  collection.find( {"best_price":{ "$gt": 0, "$lt": 250 },"date":date ,"brand":{"$in":array_brand}, "product":{"$nin":array_trash}})



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
                
                msn = (
                  
                        "✅Marca: " + str(i["brand"]) + "\n" +
                        "✅" + str(i["product"]) + list_price + "\n" +
                        "👉Precio web: " + str(i["best_price"]) + card_price + "\n" +
                        "🏷Descuento: %" + str(i["web_dsct"]) + " "+dsct+"\n\n" +
                        "🕗" + i["date"] + " " + i["time"] + "\n" +
                        "🌐Link: " + str(i["link"]) + "\n" +
                        "🏠home web: " + i["home_list"] + "\n\n" +
                        "◀️◀️◀️◀️◀️◀️◀️▶️▶️▶️▶️▶️▶️"#############################
                    )

                # msn =  "✅Marca: "+str(i["brand"])+"\n✅"+str(i["product"])+list_price+"\n👉Precio web :"+str(i["best_price"])+card_price+"\n"+dsct+"Descuento: "+"% "+str(i["web_dsct"])+"\n"+"\n\n⌛"+i["date"]+" "+ i["time"]+"\n🔗Link :"+str(i["link"])+"\n🏠home web:"+i["home_list"]+"\n\n◀️◀️◀️◀️◀️◀️◀️▶️▶️▶️▶️▶️▶️"
                foto = i["image"]
                send_telegram(msn, foto, bot_token, chat_id)
                print(chat_id)
                print(bot_token)
                print(" PRODUCTO EN BASE B NO EXISTE, SE ENVIA A TELEGRAM")
                


            if b!=a:
                #send_telegram( ("<b>Marca: "+i["brand"]+"</b>\nModelo: "+i["product"]+"\nPrecio Lista :" +str(i["list_price"])+ "\n<b>Precio web :"+str(i["best_price"])+"</b>\nPrecio Tarjeta :"+str(i["card_price"])+"\n"+i["image"]+"\nLink :"+str(i["link"])))
                print("PRODUCTO DE A ES DIFERENTE DE B,  SE ENVIA  A TELEGRAM")
               
                save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                            i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],ship_db2)
                continue
            if a==b:
                print("SON IGUALES,  NO SE ENVIA TELEGRAM")
    gc.collect()



def productos_sin_dsct( ship_db1,ship_db2, bot_token, chat_id,bd_name, collection_name):

    db = client[bd_name]
    collection = db[collection_name]

    product_shoes_patters =[
                    re.compile(r'zapatilla', re.IGNORECASE),
                    re.compile(r'sandalia', re.IGNORECASE),
                    re.compile(r'zapato', re.IGNORECASE),
            ]

    # Define the brand regex patterns
    brand_shoes_patterns = [
        re.compile(r'puma', re.IGNORECASE),
        re.compile(r'adidas', re.IGNORECASE),
        re.compile(r'reebok', re.IGNORECASE),
        re.compile(r'nike', re.IGNORECASE),
        re.compile(r'under armor', re.IGNORECASE),
        re.compile(r'hi tec', re.IGNORECASE),
        re.compile(r'Converse', re.IGNORECASE),
        re.compile(r'vans', re.IGNORECASE)
    ]

    # Define the query
    shoes = {
        "product": {"$in": product_shoes_patters},
        "brand": {"$in": brand_shoes_patterns},
        "$or": [
            {"best_price": {"$lte": 150, "$gt": 0}},
            {"list_price": {"$lte": 150, "$gt": 0}},
            {"card_price": {"$lte": 150, "$gt": 0}}
        ]
    }

    #################################################\
    product_compu_regex_patterns = [
    re.compile(r'laptop', re.IGNORECASE),
    re.compile(r'ryzen', re.IGNORECASE),
    re.compile(r'notebook', re.IGNORECASE),
    re.compile(r'tablet', re.IGNORECASE),
    re.compile(r'ipad', re.IGNORECASE)
    ]

    # Define the exclusion patterns
    exclusion_compu_patterns = [
        re.compile(r'celeron', re.IGNORECASE),
        re.compile(r'ryzen 3', re.IGNORECASE),
        re.compile(r'core i3', re.IGNORECASE),
        re.compile(r'ci3', re.IGNORECASE)
    ]

    # Define the brand regex patterns
    brand_compu_patterns = [
        re.compile(r'lenovo', re.IGNORECASE),
        re.compile(r'alien', re.IGNORECASE),
        re.compile(r'hp', re.IGNORECASE),
        re.compile(r'lg', re.IGNORECASE),
        re.compile(r'apple', re.IGNORECASE),
        re.compile(r'asus', re.IGNORECASE),
        re.compile(r'acer', re.IGNORECASE),
        re.compile(r'panasonic', re.IGNORECASE)
    ]

    # Define the query
    laptop = {
        "product": {
            "$in": product_compu_regex_patterns,
            "$not": {"$in": exclusion_compu_patterns}
        },
        "brand": {"$in": brand_compu_patterns},
        "web_dsct": 0,
        "$or": [
            {"best_price": {"$lte": 3500, "$gt": 0}},
            {"list_price": {"$lte": 3500, "$gt": 0}},
            {"card_price": {"$lte": 3500, "$gt": 0}}
        ]
    }


    # Execute the query
    lap = collection.find(laptop)
    sh = collection.find(shoes)
     
    product_array = []
    result = itertools.chain(lap, sh)
    # Iterate over the result and print each document
    for i in result:
    
        product_array.append(i)
        print(i)     
    collection_1 = db[ship_db1]
    collection_2 = db[ship_db2]
    for i in product_array:
            save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                           i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],bd_name,ship_db1)
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
                            i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],bd_name,ship_db2)
                

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
                
                msn = (
                  
                        "🌟🦙 <b>Detalles del Producto</b> 🦙🌟\n\n" +
                        "✅ <b>Marca:</b> " + str(i["brand"]) + "\n" +
                        "📦 <b>Producto:</b> " + str(i["product"]) + list_price + "\n" +
                        "👉 <b>Precio web:</b> " + str(i["best_price"]) + card_price + "\n" +
                        "🏷 <b>Descuento:</b> %" + str(i["web_dsct"]) + " " + dsct + "\n\n" +
                        "🕗 <b>Fecha y Hora:</b> " + i["date"] + " " + i["time"] + "\n" +
                        "🔗 <b>Enlace:</b> <a href='" + str(i["link"]) + "'>Link aquí</a>\n\n" 
                    )

                # msn =  "✅Marca: "+str(i["brand"])+"\n✅"+str(i["product"])+list_price+"\n👉Precio web :"+str(i["best_price"])+card_price+"\n"+dsct+"Descuento: "+"% "+str(i["web_dsct"])+"\n"+"\n\n⌛"+i["date"]+" "+ i["time"]+"\n🔗Link :"+str(i["link"])+"\n🏠home web:"+i["home_list"]+"\n\n◀️◀️◀️◀️◀️◀️◀️▶️▶️▶️▶️▶️▶️"
                foto = i["image"]
                send_telegram(msn, foto, bot_token, chat_id)
                print(chat_id)
                print(bot_token)
                print(" PRODUCTO EN BASE B NO EXISTE, SE ENVIA A TELEGRAM")
                


            if b!=a:
                #send_telegram( ("<b>Marca: "+i["brand"]+"</b>\nModelo: "+i["product"]+"\nPrecio Lista :" +str(i["list_price"])+ "\n<b>Precio web :"+str(i["best_price"])+"</b>\nPrecio Tarjeta :"+str(i["card_price"])+"\n"+i["image"]+"\nLink :"+str(i["link"])))
                print("PRODUCTO DE A ES DIFERENTE DE B,  SE ENVIA  A TELEGRAM")
               
                save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                            i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"],bd_name,ship_db2)
                continue
            if a==b:
                print("SON IGUALES,  NO SE ENVIA TELEGRAM")
    gc.collect()

    



def build_product_message(product_array):
        for i in product_array:
            save_data_to_mongo_db( i["sku"], i["brand"] , i["product"], i["list_price"], 
                          i["best_price"], i["card_price"], i["link"] ,i["image"],i["web_dsct"], i["card_dsct"],bd_name,ship_db1)
            

            if i["web_dsct"] <= 50:
                web_d = "🟡"
            if i["web_dsct"]  > 50 and i["web_dsct"]  <=69:
                web_d = "🟢"
            if i["web_dsct"]  >=70:
                web_d = "🔥🔥🔥🔥🔥🔥🔥"

            if i["card_dsct"] <= 50:
                card_d = "🟡"
            if i["card_dsct"] > 50 and i["card_dsct"]  <=69:
                card_d = "🟢"
            if i["card_dsct"]  >=70:
                card_d = "🔥🔥🔥🔥🔥🔥🔥"

            
            if i["list_price"] == 0:
                list_price = ""
            else:
                list_price = '🏷 <b>Precio lista:</b> '+  str(i["list_price"])+"\n" 
            
            if i["best_price"] == 0:
                best_price = ""
            else:
                best_price = '👉 <b>Precio web:</b> <b>'+ str(i["best_price"]) + "</b>" +"\n" 

            if i["card_price"] == 0:
                card_price = ""
            else:
                card_price = '💳 <b>Precio TC:</b> <b>' +str(i["card_price"])+ "</b>"+"\n" 

            if i["card_dsct"] == 0:
                card_dsct = ""
            else:
                card_dsct =  "💥 <b>Descuento TC:</b> %" + str(i["card_dsct"])+ card_d+"\n" 

            if i["web_dsct"] == 0:
                web_dsct = ""
            else:
                web_dsct =   "💵 <b>Descuento web:</b> %" + str(i["web_dsct"])+ web_d+  "\n" 
    
            
            

            msn = (
                
                    "🌟🦙 <b>Detalles del Producto</b> 🦙🌟\n\n" +
                    "✅ <b>Marca:</b> " + str(i["brand"]) + "\n" +
                    "📦 <b>Producto:</b> " + str(i["product"])  + "\n\n" +
                    list_price+
                    best_price +
                    card_price+
                    "\n"+
                    card_dsct+
                    web_dsct+
                    "🕗 <b>Fecha y Hora:</b> " + i["date"] + " " + i["time"] + "\n" +
                    "🔗 <b>Enlace:</b> <a href='" + str(i["link"]) + "'>Link aquí</a>\n\n" 
            )
           

# Envía este mensaje_telegram como respuesta en tu código para Telegram

            foto = i["image"]

            print(len(foto))


            if len(foto) <5:
                print(len(foto))
                foto="https://westsiderc.org/wp-content/uploads/2019/08/Image-Not-Available.png"

            
            
          
           










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