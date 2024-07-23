from decouple import config
import telegram
import logging
# from delete_past_dats import delete_pastdays
# from delete_collection import reset_products
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from register import     register_safa
import unicodedata
import time
from  telegram_search_engine import auto_product
import re


from search_bot_service import busqueda, search_brand_dsct, auto_telegram, delete_brand,add_brand_list,read_category,manual_telegram, search_market_dsct,search_market2_dsct, search_product_dsct_html, search_brand_dsct_html,read_brands,cat_search

def super_bot(TOKEN, bot_token ,chat_id, db1,db2):
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s -  %(message)s,")
    logger = logging.getLogger()

    ### 1 ENVIA EL STATUS DEL BOT 
    def getBotInfo(update, context):
        bot = context.bot
        chatId= update.message.chat_id

        userName = update.effective_user["first_name"]
        logger.info(f"el usuario {userName} ha solicitado informacion sobre el bot " +str(chatId) )
        print(context.args)
        
        bot.sendMessage(
            chat_id=chatId,
            parse_mode="HTML",text= f"Hola soy un bot creado para la Nave por Sr Spok. sigo funcionando no te preocupes❗❗❗ "
            #,message_thread_id="5"
        )

    # ### 2 ENVIA LOS COMANDOS DEL BOT 
    # def Commands(update, context):
        bot = context.bot
        chatId= update.message.chat_id
        userName = update.effective_user["first_name"]
        logger.info(f"el usuario {userName} ha solicitado informacion sobre el bot " +str(chatId))
        print(context.args)
        
        bot.sendMessage(
            chat_id=chatId,
            parse_mode="HTML",
            text= f"#################\n LISTA DE COMANDOS\n #################\n \n >Marca y porcentaje (Telegram)\n /b marca %   \n \n >Palabra  y % (HTML)\n /product palabra %\n \n >Tienda y %  (HTML)\n /send tienda %\n \n >Tienda y %  (Telegram)\n /market tienda % \n \n >Codigo de producto (Telegram)\n /cod codigo_de_producto\n \n >Busca y envia variacion o nuevo (Telegram)\n /auto categoria  (Telegram)\n \n >Busca toda categoria 60% (Telegram)\n /manual categoria % (Telegram)\n \n >Agrega marca a categoria(Telegram)\n /brand marca categoria\n \n >Elimina marca a categoria(Telegram)\n /delete marca categoria"
        )

    ### 3 SE ECARGA DE DAR AUTOMATICAMENTE LA BIENVENIDA A LOS NUEVOS INTEGRANTES 
    def welcomeMsg(update, context):
        bot = context.bot
        chatId = update.message.chat_id
        updateMsg= getattr(update, "message", None)
        for user in updateMsg.new_chat_members:
            userName = user.first_name
        
        logger.info(f"El usuario {userName} ha ingresado al grupo" )

        bot.sendMessage(
            chat_id= chatId,
            parse_mode= "HTML",
            text=f"Bienvenido al grupo {userName}."
        )

    # ### 4 BUSCA EN BASE A MARCA Y DESCUENTO 
    # ###   USANDO EL COMANDO  " /b "
    # def custom_search(update, context):
    #     bot = context.bot
    #     chatId= update.message.chat_id
    #     userName = update.effective_user["first_name"]
    #     logger.info(f"el usuario {userName} ha solicitado una buesqueda")
    #     brand= (context.args[0]).replace("%"," ")
    #     dsct=int(context.args[1])
    #     if dsct <= 41:
    #        dsct = 40

    #     bot.sendMessage(
    #         chat_id=chatId,
    #         parse_mode="HTML",
    #         text= f"Procesado busqueda..."
    #     )
    #     search_brand_dsct(brand, dsct, bot_token ,chat_id)

    #     bot.sendMessage(
    #         chat_id=chatId,
    #         parse_mode="HTML",
    #         text= f"Se realizo busqueda de la marca ingresada "+ str(brand) +" de "+ str(dsct) + "%  a mas\n\n#####################################\n#####################################"
    #     )

    # ### 5 BUSCA EN BASE A MARKET Y DESCUENTO
    # def custom_search_market(update, context):
    #     bot = context.bot
    #     chatId= update.message.chat_id
    #     userName = update.effective_user["first_name"]
    #     logger.info(f"el usuario {userName} ha solicitado una buesqueda")
    #     try: 
    #         market= (context.args[0]).replace("%"," ")
    #     except IndexError:
    #          market = None
    #     try:
    #         dsct = int(context.args[1])
    #         if dsct <= 41:
    #              dsct = 40
    #     except IndexError:
    #          dsct = None

    #     if dsct == None or market == None:
    #         bot.sendMessage(
    #         chat_id=chatId,
    #         parse_mode="HTML",
    #         text= f"Falta market o descuento.... ejemplo:  /market metro 50"
    #         )

    #     if market and dsct != None:
            
    #         bot.sendMessage(
    #             chat_id=chatId,
    #             parse_mode="HTML",
    #             text= f"Procesnado busquerda..."
    #             )

    #         search_market_dsct(str(market), int(dsct), bot_token ,chat_id)
    #         #logger.info(f"marca "+ market + "dsct "+ str(dsct))

    #         bot.sendMessage(
    #             chat_id=chatId,
    #             parse_mode="HTML",
    #             text= f"Se realizo busqueda de la marca ingresada"+ str(market) +" de "+ str(dsct) + "%  a mas\n\n#####################################\n#####################################"
    #             )
            

    # ### 7 BUSCA EN PRODUCTO CON EL CODIGO SKU
    def sku(update, context):
        bot = context.bot
        chatId= update.message.chat_id
        userName = update.effective_user["first_name"]
        logger.info(f"el usuario {userName}  busca codigo especifico")
        codigo = context.args[0]


        bot.sendMessage(
            chat_id=chatId,
            parse_mode="HTML",
            text= f"Procesado busqueda..."
        )
        
        busqueda(str(codigo), bot_token ,chat_id)
        bot.sendMessage(
            chat_id=chatId,
            parse_mode="HTML",
            text= f"Termino la busqueda... si no hay nada no encontre ps"
        )

    # ### 8 BUSCA AUTOMATICAMENTE LAS MARCAS EN LAS CATEGORIAS DEL 60% EN ADELANTE NO ENVIA SI YA SE ENVIO
    # def auto_tele(update, context):
    #     bot = context.bot
    #     chatId= update.message.chat_id
    #     userName = update.effective_user["first_name"]
    #     logger.info(f"el usuario {userName}  busqueda automatica")

    #     category=str(context.args[0])

    #     bot.sendMessage(
    #         chat_id=chatId,
    #         parse_mode="HTML",
    #         text= f"Espera un momento se esta procesando la solicitud "
    #     )
        

    #     auto_telegram( category,db1, db2 ,bot_token ,chat_id,70)

    #     bot.sendMessage(
    #         chat_id=chatId,
    #         parse_mode="HTML",
    #         text= f"Se termino la busqueda "
    #     )
    #     logger.info(f"se Termino la Busqueda")
        



    # ### 9 ENVIA PRODUCTOS QUE HAY EN UNA CARTEGORIAS 
    # def category_list(update, context):
    #     bot = context.bot
    #     chatId= update.message.chat_id
    #     userName = update.effective_user["first_name"]
    #     logger.info(f"el usuario {userName} ha solicitado una buesqueda")
    #     read_category(bot_token ,chat_id)


    # def brand_list(update, context):
    #     bot = context.bot
    #     chatId= update.message.chat_id
    #     userName = update.effective_user["first_name"]
    #     logger.info(f"el usuario {userName} ha solicitado una buesqueda")
    #     category=context.args[0]
    #     read_brands(category,bot_token ,chat_id)


    # ### 10 AÑADE MARCA A UNA CATEGORIA SELECCIONADA
    # def add_brand(update, context):
    #     bot = context.bot
    #     chatId= update.message.chat_id
    #     userName = update.effective_user["first_name"]
    #     logger.info(f"el usuario {userName} ha solicitado una buesqueda")
    #     brand= (context.args[0]).replace("%"," ")
        
    #     category=(context.args[1]).replace("%","")
    #     add_brand_list(brand, category,bot_token ,chat_id)

    #     bot.sendMessage(
    #         chat_id=chatId,
    #         parse_mode="HTML",
    #         text= f"Se agrego al buscador de "+str(category)+" la "+str(brand)
    #     )

    # ### 11 ELIMINA MARCA DE CARTEGORIA
    # def brand_delete(update,context):
    #     bot = context.bot
    #     chatId= update.message.chat_id
    #     userName = update.effective_user["first_name"]
    #     logger.info(f"el usuario {userName}  se elimina  marca")
    #     brand=(context.args[0])
    #     category=context.args[1]

    #     delete_brand(brand,category,bot_token ,chat_id)


    # ### 12 BUSCA TODAS LAS MARCAS SEGUN CATEGORIA MANUALMENTE CON DESCUENTO PERSONALIZADO
    # def auto_tele_dsct(update, context):
    #     bot = context.bot
    #     chatId= update.message.chat_id
    #     userName = update.effective_user["first_name"]
    #     logger.info(f"el usuario {userName}  buscqueda automatica")
    #     category=str(context.args[0])
    #     dsct=int(context.args[1])
    #     bot.sendMessage(
    #         chat_id=chatId,
    #         parse_mode="HTML",
    #         text= f"Espera un momento se esta procesando la solicitud "
    #     )
        
    #     manual_telegram( category,dsct ,bot_token ,chat_id)

    #     bot.sendMessage(
    #         chat_id=chatId,
    #         parse_mode="HTML",
    #         text= f"Se termino la busqueda "
    #     )
    #     logger.info(f"se Termino la Busqueda")


    ### 13 CREA HTML DE BUSQUEDA DE MARKET Y DSCT PERSONALIZADO
    def send_document(update, context):
        bot = context.bot
        chat_id = update.message.chat_id
        userName = update.effective_user["first_name"]
        logger.info(f"el usuario {userName} ha solicitado una buesqueda")

        market = (context.args[0])
        print(market)
        shop = ["saga","plazavea", "shopstar", "ripley", "coolbox", "wong", "metro", "tailoy", "promart", "oechsle", "hiraoka", "curacao", "platanitos", "all"]
        if market not in shop:
            bot.sendMessage(
            chat_id=chat_id,
            parse_mode="HTML",
            text= f"Ese market no es ninguno de los siguientes saga, shopstar, plzavea, ripley, coolbox, wong, metro, tailoy, promart, oechsle, hiraoka, curacao, platanitos..."
                )
            return

       
        dsct=int(context.args[1])

        dsct = int(dsct)
        print(dsct)
     
        try:
         price = (context.args[2])
        except: price = None

        bot.sendMessage(
            chat_id=chat_id,
            parse_mode="HTML",
            text= f"Procesado busqueda..."
        )

        search_market2_dsct(market,dsct,price, bot_token ,chat_id)

        document = open(config("HTML_PATH")+market+".html", 'rb')
        context.bot.send_document(chat_id, document)
        document.close()
        os.remove(config("HTML_PATH")+market+".html")
        print("pasa por aqui")
       
      
        
    ### 14 CREA HTML DE BUSQUEDA DE PALABRA CONTENIDA EN EL NOMBRE DEL PRODUCTO Y DSCT PERSONALIZADO POSIBLE ORDENAR PRECIO MAYOR A MENOR
    def send_product(update, context):
        chat_Id = update.message.chat_id
        userName = update.effective_user["first_name"]
        bot = context.bot
        logger.info(f"el usuario {userName} ha solicitado una buesqueda")

        # product = (context.args[0]).replace("%"," ")

        # db_name = (context.args[1])

        # print(product)
        # print(db_name)
        # input("Asasaas")
        #dsct=int(context.args[1])
        text = update.message.text
        words = text.split()

        product = words[1]
        dsct = words[2]
    


        # print(words)
        # if not words:
        #     # handle error
        #     return
        
        #product = " ".join(words).replace("/product","")

      
     

        # try:
        #     dsct = int(words[-1])
        # except: 
        #     bot.sendMessage( chat_id=chat_Id, parse_mode="HTML", text= f"Falta el Descuento" )
                    

    # do something with the arguments here
    
        # try:
        #  price = (context.args[2])
        # except: price = None
        price = None
        print(product)  
        print(dsct)
        bot.sendMessage(
            chat_id=chat_Id,
            parse_mode="HTML",
            text= f"Procesado busqueda..."
        )
        


        search_product_dsct_html(product,dsct,price ,bot_token ,chat_Id)

        document = open(config("HTML_PATH")+product+".html", 'rb')
        context.bot.send_document(chat_Id, document)
        document.close()
        os.remove(config("HTML_PATH")+product+".html")


    ### 14 CREA HTML DE BUSQUEDA DE MARCA Y DSCT PERSONALIZADO
    def brand_to_html(update, context):
        chat_Id = update.message.chat_id
        bot = context.bot
        userName = update.effective_user["first_name"]
        logger.info(f"el usuario {userName} ha solicitado una buesqueda")

        # brand = (context.args[0]).replace("%"," ")
        # dsct=int(context.args[1])
        # dsct = int(dsct)
        ##################
        text = update.message.text
        print(text)
        words = text.split()
        if not words:
            # handle error
            return
        
        brand = " ".join(words[:-1]).replace("/marca","").lstrip()
        print(words)
        try:
            dsct = int(words[-1])
        except: 
            bot.sendMessage( chat_id=chat_Id, parse_mode="HTML", text= f"Falta el Descuento" )
    ###########
        # try:
        #  price = (context.args[2])
        # except: price = None
        price = None

        search_brand_dsct_html(brand,dsct,price, bot_token ,chat_id)

        document = open(config("HTML_PATH")+brand+".html", 'rb')
        context.bot.send_document(chat_id, document)
        document.close()
        os.remove(config("HTML_PATH")+brand+".html")






    def find(update, context):
        chat_Id = update.message.chat_id

        bot = context.bot
        userName = update.effective_user["first_name"]
        logger.info(f"el usuario {userName} ha solicitado una buesqueda")
        porcentage1 = 40
        porcentage2 = 59

        # brand = (context.args[0]).replace("%"," ")
        # dsct=int(context.args[1])
        # dsct = int(dsct)
        ##################
        text = update.message.text
       
        product = text.split()
        if not product:
            # handle error
            return
        
        if product[0] != "/find":
             bot.sendMessage( chat_id=chat_Id, parse_mode="HTML", text= f"comando incorrecto" )

        product = product[1]

        #product = " ".join(product[:-1]).replace("/find","").lstrip()
        print(product)
        #auto_product()
        auto_product(  "cupo1","cupo2", bot_token, chat_id,porcentage1, porcentage2, product)


       
    
 

    ### 14 CREA HTML DE BUSQUEDA DE MARCA Y DSCT PERSONALIZADO
    # def fazil_reg(update, context):
    #     user_id = update.message.from_user.id
    #     chat_id = update.message.chat_id
    #     message_text = update.message.text
    #     userName = update.effective_user["first_name"]
    #     logger.info(f"el usuario {userName} ha solicitado una buesqueda")
    #     bot = context.bot
       
    #     var = message_text
    #     var = var[2:]
    #     var = var.split()
     

    #     if len(var) < 4:
    #             bot.sendMessage(
    #         chat_id=chat_id,
    #         parse_mode="HTML",text= f"Faltan datos para crear la cuenta de fazil "
    #         #,message_thread_id="5"
    #          )

    #     name = (var[0])
    #     last_name= (var[1])

 
    #     normalizada = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('utf-8')
    #     normalizada2 = unicodedata.normalize('NFKD', last_name).encode('ASCII', 'ignore').decode('utf-8')
    #     if normalizada.isalpha() and normalizada2.isalpha():
    #         print("La cadena contiene solo letras (sin acentos)")
    #     else:
    #        bot.sendMessage(
    #             chat_id=chat_id,
    #             parse_mode="HTML",text= f"Formato incorrecto: /f nombre appelido celular email"
    #             )
    #        name = None;last_name = None


       
    #     #dni=str(var[2])
    #     cel=str(var[2])
    #     if cel.isdigit() and len(cel) == 9:
    #         print("The string contains only numbers and 9 digits")
    #     else:
    #         bot.sendMessage(
    #             chat_id=chat_id,
    #             parse_mode="HTML",text= f"Formato incorrecto: /f nombre appelido celular email, el celular solo debe tener 9 digitos"
    #             )
    #         cel = None
            


    #     email=str(var[3])
    #     pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    #     if re.match(pattern, email):
    #         print("La dirección de correo electrónico es válida")
    #     else:
    #         bot.sendMessage(
    #             chat_id=chat_id,
    #             parse_mode="HTML",text= f"Formato incorrecto: /f nombre appelido celular email, formato de email incorrecto"
    #             )
    #         email = None
            
    #     #pwd=str(var[5])
    #     if name or last_name or cel or email == None:
    #         print(" error de data input")

    #     if name and last_name and cel and email:
    #         fazil = register_safa(name,last_name,cel,email)
    
    #         bot.sendMessage(
    #                     chat_id=chat_id,
    #                     parse_mode="HTML",text= f"Creando cuenta Fazil"
                
    #                     )
            
    #         if fazil == False:
    #                  bot.sendMessage(
    #                 chat_id=chat_id,
    #                 parse_mode="HTML",text= f"El correo ya existe"
    #                 )
                     
    #         if fazil == True:
    #              bot.sendMessage(
    #                 chat_id=chat_id,
    #                 parse_mode="HTML",text= f"Error de Sincronizacion al estilo de Saga falabella, Intenta de nuevo"
    #                 )
                     
    #         if fazil =="paso":
    #             bot.sendMessage(
    #             chat_id=chat_id,
    #             parse_mode="HTML",text= f" Ya se creo cuenta exitosamente"
    
    #             )

    # def delete_past_database(update, context):
    #         bot = context.bot
    #         chatId= update.message.chat_id
    #         delete_pastdays()
         

    #         userName = update.effective_user["first_name"]
    #         logger.info(f"el usuario {userName} ha solicitado informacion sobre el bot " +str(chatId) )
    #         print(context.args)
            
    #         bot.sendMessage(
    #             chat_id=chatId,
    #             parse_mode="HTML",text= f"Se elimino limpio base de datos❗❗❗ "
          
    #         )

      
       
    # def reset_ship_data(update, context):

    #     bot = context.bot
    #     chatId= update.message.chat_id
    #     collection_data=str(context.args[0])

    #     reset_products(collection_data)

    #     bot.sendMessage(
    #             chat_id=chatId,
    #             parse_mode="HTML",text= f"Se resteo todo los productos enviados a la nave especificada❗ "
          
    #         )
        
    # def category_search(update, context):

    #     bot = context.bot
    #     chatId= update.message.chat_id
    #     category=str(context.args[0])
    #     dsct=str(context.args[1])

    #     cat_search(category, dsct ,bot_token ,chat_id)

    #     document = open(config("HTML_PATH")+category+".html", 'rb')
    #     context.bot.send_document(chat_id, document)
    #     document.close()
    #     os.remove(config("HTML_PATH")+category+".html")
    #     print("pasa por aqui")
       

    #     bot.sendMessage(
    #             chat_id=chatId,
    #             parse_mode="HTML",text= f" busqueda de categoria al de "+dsct+" a 100❗ "
          
    #         )





    # if __name__ == "__main__":
    myBot = telegram.Bot(token = TOKEN)
    print(myBot.getMe())

    updater = Updater(myBot.token, use_context=True)

    dp= updater.dispatcher
    dp.add_handler(CommandHandler("botinfo", getBotInfo))
    # dp.add_handler(CommandHandler("comandos", Commands))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcomeMsg))
    # dp.add_handler(CommandHandler('b', custom_search))
    dp.add_handler(CommandHandler("send", send_document))
    # dp.add_handler(CommandHandler("clean", delete_past_database))
    # dp.add_handler(CommandHandler("resetship", reset_ship_data))
    dp.add_handler(CommandHandler("product", send_product))
    # dp.add_handler(CommandHandler('market', custom_search_market))
    dp.add_handler(CommandHandler('cod', sku))
    dp.add_handler(CommandHandler('find', find))
    # dp.add_handler(CommandHandler("f", fazil_reg))
    # dp.add_handler(CommandHandler('manual', auto_tele_dsct))
    # dp.add_handler(CommandHandler('category', category_search))
    # dp.add_handler(CommandHandler('brand', add_brand))
    # dp.add_handler(CommandHandler('delete', brand_delete))
    # dp.add_handler(CommandHandler('cat', category_list))
    # dp.add_handler(CommandHandler('catlist', brand_list))
    dp.add_handler(CommandHandler('marca', brand_to_html))


    updater.start_polling()
    updater.idle()