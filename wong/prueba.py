#https://api.telegram.org/
#https://core.telegram.org/bots/api
import sys
sys.path.append('/Users/javier/GIT/fala') 
from math import prod
from multiprocessing.forkserver import connect_to_new_process
import time
import requests
from pymongo import MongoClient
import os
import ast



mensaje = "No me pegues Lucero....."


def send_telegram(message):
    requests.post("https://api.telegram.org/bot5504401191:AAG8Wuk5AF95qEWn0642ZjhzduE0CbVkBaU/sendMessage",
                
    data= {'chat_id': '-1001765171182','text': str(message)  }  )


    
    
    
MONGO_URI = "mongodb+srv://legion:Legi0n$.2022@cluster0.spmg6.mongodb.net/?retryWrites=true&w=majority"
MONGO_LOCAL = "mongodb://superuser:Viper.2013@192.168.9.66:27017/?authMechanism=DEFAULT&tls=false"
client = MongoClient(MONGO_LOCAL)

        
db = client["cencosud"]
collection = db["market"] 

## QUERYS DE MONGO PARA BUSCAR OFERTAS O PRECIOS BUGS 
x = collection.find({   "description":{"$regex" : '55"' }, "best_price":{"$lte":1000, "$ne":0}    })
y = collection.find({   "description":{"$regex" : '50"' }, "best_price":{"$lte":1000, "$ne":0}  })
z = collection.find({   "description":{"$regex" : '65"' }, "best_price":{"$lte":1000, "$ne":0}  })
r= collection.find({ "description":{"$regex":'70"'}, "best_price":{"$lte":1500, "$ne":0}  })
t = collection.find({ "description":{"$regex":'75"'}, "best_price":{"$lte":1500, "$ne":0}  })
l = collection.find({   "description":{"$regex" :'lavadora',"$options":"i"}, "best_price":{"$lte":700, "$ne":0}  })
c=collection.find({"description":{"$regex" :'refrigeradora',"$options":"i"}, "best_price":{"$lte":1000, "$ne":0}})
f= collection.find({   "description":{"$regex" :'ryzen',"$options":"i"}, "best_price":{"$lte":3300, "$ne":0}, "category":{"$regex":"laptop","$options":"i" } })
l1= collection.find({   "description":{"$regex" :'i7',"$options":"i"}, "best_price":{"$lte":1300, "$ne":0}, "category":{"$regex":"laptop","$options":"i" } })
l2= collection.find({   "description":{"$regex" :'i5',"$options":"i"}, "best_price":{"$lte":1300, "$ne":0}, "category":{"$regex":"laptop","$options":"i" } })
l3= collection.find({   "description":{"$regex" :'i3',"$options":"i"}, "best_price":{"$lte":1300, "$ne":0}, "category":{"$regex":"laptop","$options":"i" } })

pro = [x,y,z,r,t,l,c,f,l1,l2,l3]  ## ARREGLO DE LOS QUERYS DE MONGO PARA MANDAR POR TELEGRAM
products = []

## FUNCION QUE COLOCA EN UNA LISTA (products) TODO LOS PRODUCTOS PARA SER MANDADOS A TELEGRAM,
## AQUI SE LE PASA EL OBJETO  MONGO PARA ITERACION Y EXTRACCIONDE LOS CAMPOS
def mongodb_search():
    for idx, value in enumerate(pro):
        for i in value:
            mongo_obj = [   i["image"], i["brand"] , i["description"], i["list_price"], 
                            i["best_price"], i["card_price"], i["link"]  
                        ]
            #print(val)
            products.append(mongo_obj)
            time.sleep(2)
    #print(products)
    
    
## ESTA FUNCION ITERA LOS OBJETOS QUERY EN LA FUNCION MONGODB_SEARCH Y FILTRA LOS MENSAJES REPETIDOS
## Y MANDA  SI HAY PRODUCTOS NUEVOS O SI SON REPETIDOS NO MANDA NADA
#########################################################################################

new_array=[]
def auto_tele():
         
    file = open("/Users/javier/GIT/fala/wong/listA.txt" , "r") 
    content = file.read()
    try:
     content = ast.literal_eval(content)
    except: content = None

    print(type(content))
    print(content)
    print()
    print(products)
    print(type(products))
  
    if content == None:
        for i,v in enumerate(products):
          send_telegram(v)
        print( " SE ENVIA POR PRIMERA VEZ EL MENSAJE A TELEGRA,")
     
    if content == products:
        print(" SON IGUALES LOS ARREGLOS NO SE ENVIA NADA")
        # print(content)
      

    if content != products and content != "":
        new_array = [elem for elem in content if elem not in products]
        print(new_array)
        for i,v in enumerate(new_array):
            send_telegram(v)
            
    

    # if content != products and content != "":
    #     setA = set(products)
    #     setB = set(content)
    #     print()
    #     print(setA)
    #     print(setB)
    #     if setA > setB:
    #         x = setA-setB
    #         new_array.append(x)
    #     for i,v in enumerate(new_array):
    #             send_telegram(v)
            
    #     else:
    #         x = setB-setA 
    #         new_array.append(x)
    #     for i,v in enumerate(new_array):
    #             send_telegram(v)

        print("no son iguales")
        
        file = open("/Users/javier/GIT/fala/wong/listA.txt" , "w+") 
        content = str(new_array)
        file.write(content)
        file.close()


    
mongodb_search()
auto_tele()



