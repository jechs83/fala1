import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import sys



count = 0

for imn in range (100):
  count = count+1

  print(count)

    
    
    

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

