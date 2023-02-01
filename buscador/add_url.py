from pymongo import MongoClient
from decouple import config
from datetime import datetime
from telegram import ParseMode
from decouple import config
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters





client = MongoClient(config("MONGO_DB"))
# db5 = client["scrap"]
# collection5 = db5["scrap"] 


def add_url_db(market,id,url):

        db = client[market]
        collection= db["lista"]

        x = collection.find_one({"_id":int(id)})
      
        if x  :
            #print(" ACTUALIZA BASE DE DATOS ")
            filter = {"_id":int(id)}
            newvalues = { "$push":{ 
            "url":url
            
            }   
           
            }
            collection.update_many(filter,newvalues)    

        else:

            data = {
            "_id":int(id),
            "url":[url]
            
            }   
           
        
            collection.insert_one(data) 



def urls_per_market(market):


    db = client[market]
    collection= db["lista"]

    x = collection.find({})
    number_list = []
    for i in x:
        n_list =i["_id"]
        #number_list.append(n_list)


        y = collection.find({"_id":n_list})

        for i in y:
            s = len(i["url"])

            f = str(n_list) , str(s)
            number_list.append(f)
        

    return(len(number_list))


def listToString(s):
         
            # initialize an empty string
            str1 = ""
        
            # traverse in the string
            for ele in s:
                str1 += ele
        
            # return string
            return str1

def view_url(market,id):
        list = []
        db = client[market]
        collection= db["lista"]

        x = collection.find({"_id":id})
             
        for i in x:

            r= i["url"]
            list.append(r)
        f = listToString(list)

        print(f)
        
     
view_url("juntoz", 4)


