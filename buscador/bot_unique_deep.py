from decouple import config
import telegram
import logging
from delete_past_dats import delete_pastdays
from delete_collection import reset_products
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from register import     register_safa
import unicodedata
import re


from search_bot_service import busqueda, search_brand_dsct, auto_telegram, delete_brand,add_brand_list,read_category,manual_telegram, search_market_dsct,search_market2_dsct, search_product_dsct_html, test2, search_brand_dsct_html,read_brands,search_price

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

### 2 ENVIA LOS COMANDOS DEL BOT 
    def Commands(update, context):
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

### 4 BUSCA EN BASE A MARCA Y DESCUENTO 
###   USANDO EL COMANDO  " /b "
    def custom_search(update, context):
        bot = context.bot
        chatId= update.message.chat_id
        userName = update.effective_user["first_name"]
        logger.info(f"el usuario {userName} ha solicitado una buesqueda")
        brand= (context.args[0]).replace("%"," ")
        dsct=int(context.args[1])
        if dsct <= 41:
           dsct = 40

        bot.sendMessage(
            chat_id=chatId,
            parse_mode="HTML",
            text= f"Procesado busqueda..."
        )
        search_brand_dsct(brand, dsct, bot_token ,chat_id)

        bot.sendMessage(
            chat_id=chatId,
            parse_mode="HTML",
            text= f"Se realizo busqueda de la marca ingresada "+ str(brand) +" de "+ str(dsct) + "%  a mas\n\n#####################################\n#####################################"
        )

### 5 BUSCA EN BASE A MARKET Y DESCUENTO
    def custom_search_market(update, context):
        bot = context.bot
        chatId= update.message.chat_id
        userName = update.effective_user["first_name"]
        logger.info(f"el usuario {userName} ha solicitado una buesqueda")
        try: 
            market= (context.args[0]).replace("%"," ")
        except IndexError:
             market = None
        try:
            dsct = int(context.args[1])
            if dsct <= 41:
                 dsct = 40
        except IndexError:
             dsct = None

        if dsct == None or market == None:
            bot.sendMessage(
            chat_id=chatId,
            parse_mode="HTML",
            text= f"Falta market o descuento.... ejemplo:  /market metro 50"
            )

        if market and dsct != None:
            
            bot.sendMessage(
                chat_id=chatId,
                parse_mode="HTML",
                text= f"Procesnado busquerda..."
                )

            search_market_dsct(str(market), int(dsct), bot_token ,chat_id)
            #logger.info(f"marca "+ market + "dsct "+ str(dsct))

            bot.sendMessage(
                chat_id=chatId,
                parse_mode="HTML",
                text= f"Se realizo busqueda de la marca ingresada"+ str(market) +" de "+ str(dsct) + "%  a mas\n\n#####################################\n#####################################"
                )

### 6 ALERTA A TODOS EN EL GRUPO  
    def alert_all(update, context):
        bot = context.bot
        chatId= update.message.chat_id
        userName = update.effective_user["first_name"]
        logger.info(f"el usuario {userName}  mando alerta a todos")

        bot.sendMessage(
            chat_id=chatId,
            parse_mode="HTML",
            text= f"@Kokotinaa @Vulcannnn @Sr_toto @Rcmed @Chucky_3  @Kaiesmipastor @lalilove9 @JkingM14 @Lachicadelascajas @Lunitaaa_0 @CarLiTuxD "
        )

### 7 BUSCA EN PRODUCTO CON EL CODIGO SKU
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

### 8 BUSCA AUTOMATICAMENTE LAS MARCAS EN LAS CATEGORIAS DEL 60% EN ADELANTE NO ENVIA SI YA SE ENVIO
    def auto_tele(update, context):
        bot = context.bot
        chatId= update.message.chat_id
        userName = update.effective_user["first_name"]
        logger.info(f"el usuario {userName}  busqueda automatica")

        category=str(context.args[0])

        bot.sendMessage(
            chat_id=chatId,
            parse_mode="HTML",
            text= f"Espera un momento se esta procesando la solicitud "
        )
        

        auto_telegram( category,db1, db2 ,bot_token ,chat_id,70)

        bot.sendMessage(
            chat_id=chatId,
            parse_mode="HTML",
            text= f"Se termino la busqueda "
        )
        logger.info(f"se Termino la Busqueda")
        



### 9 ENVIA PRODUCTOS QUE HAY EN UNA CARTEGORIAS 
    def category_list(update, context):
        bot = context.bot
        chatId= update.message.chat_id
        userName = update.effective_user["first_name"]
        logger.info(f"el usuario {userName} ha solicitado una buesqueda")
        read_category(bot_token ,chat_id)


    def brand_list(update, context):
        bot = context.bot
        chatId= update.message.chat_id
        userName = update.effective_user["first_name"]
        logger.info(f"el usuario {userName} ha solicitado una buesqueda")
        category=context.args[0]
        read_brands(category,bot_token ,chat_id)


### 10 AÑADE MARCA A UNA CATEGORIA SELECCIONADA
    def add_brand(update, context):
        bot = context.bot
        chatId= update.message.chat_id
        userName = update.effective_user["first_name"]
        logger.info(f"el usuario {userName} ha solicitado una buesqueda")
        brand= (context.args[0]).replace("%"," ")
        
        category=(context.args[1]).replace("%","")
        add_brand_list(brand, category,bot_token ,chat_id)

        bot.sendMessage(
            chat_id=chatId,
            parse_mode="HTML",
            text= f"Se agrego al buscador de "+str(category)+" la "+str(brand)
        )

### 11 ELIMINA MARCA DE CARTEGORIA
    def brand_delete(update,context):
        bot = context.bot
        chatId= update.message.chat_id
        userName = update.effective_user["first_name"]
        logger.info(f"el usuario {userName}  se elimina  marca")
        brand=(context.args[0])
        category=context.args[1]

        delete_brand(brand,category,bot_token ,chat_id)


### 12 BUSCA TODAS LAS MARCAS SEGUN CATEGORIA MANUALMENTE CON DESCUENTO PERSONALIZADO
    def auto_tele_dsct(update, context):
        bot = context.bot
        chatId= update.message.chat_id
        userName = update.effective_user["first_name"]
        logger.info(f"el usuario {userName}  buscqueda automatica")
        category=str(context.args[0])
        dsct=int(context.args[1])
        bot.sendMessage(
            chat_id=chatId,
            parse_mode="HTML",
            text= f"Espera un momento se esta procesando la solicitud "
        )
        
        manual_telegram( category,dsct ,bot_token ,chat_id)

        bot.sendMessage(
            chat_id=chatId,
            parse_mode="HTML",
            text= f"Se termino la busqueda "
        )
        logger.info(f"se Termino la Busqueda")


### 13 CREA HTML DE BUSQUEDA DE MARKET Y DSCT PERSONALIZADO
    def send_document(update, context):
        bot = context.bot
        chat_id = update.message.chat_id
        userName = update.effective_user["first_name"]
        logger.info(f"el usuario {userName} ha solicitado una buesqueda")

        market = (context.args[0]).replace("%"," ")
        dsct=int(context.args[1])
        dsct = int(dsct)
     
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

        #product = (context.args[0]).replace("%"," ")
        #dsct=int(context.args[1])
        text = update.message.text
        words = text.split()
        if not words:
            # handle error
            return
        
        product = " ".join(words[:-1]).replace("/product","")

        try:
            dsct = int(words[-1])
        except: 
            bot.sendMessage( chat_id=chat_Id, parse_mode="HTML", text= f"Falta el Descuento" )
                    

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

        document = open(config("HTML_PATH")+"producto.html", 'rb')
        context.bot.send_document(chat_Id, document)
        document.close()
        os.remove(config("HTML_PATH")+"producto.html")


### 15 PARA JODER 
    def joder(update, context):
        bot = context.bot
        chatId= update.message.chat_id
        userName = update.effective_user["first_name"]
        logger.info(f"el usuario {userName} ha solicitado informacion sobre el bot " +str(chatId))
        print(context.args)

        bot.sendMessage(
            chat_id=chatId,
            parse_mode="HTML",
            text= f""
        )


### 14 CREA HTML DE BUSQUEDA DE MARCA Y DSCT PERSONALIZADO
    def brand_to_html(update, context):
        chat_id = update.message.chat_id
        userName = update.effective_user["first_name"]
        logger.info(f"el usuario {userName} ha solicitado una buesqueda")

        brand = (context.args[0]).replace("%"," ")
        dsct=int(context.args[1])
        dsct = int(dsct)
     
        try:
         price = (context.args[2])
        except: price = None

        search_brand_dsct_html(brand,dsct,price, bot_token ,chat_id)

        document = open(config("HTML_PATH")+brand+".html", 'rb')
        context.bot.send_document(chat_id, document)
        document.close()
        os.remove(config("HTML_PATH")+brand+".html")



### TEST BUSCA EN PRODUCTO CON EL CODIGO SKU
    def test(update, context):
        bot = context.bot
        chatId= update.message.chat_id
        userName = update.effective_user["first_name"]
        logger.info(f"el usuario {userName}  busca codigo especifico")
        codigo = context.args[0]
        
        test2(str(codigo), bot_token ,chat_id)
        bot.sendMessage(
            chat_id=chatId,
            parse_mode="HTML",
            text= f"Termino la busqueda... si no hay nada no encontre ps"
        )
        
    
    ### 11 ELIMINA MARCA DE CARTEGORIA
    def restart_bot(update,context):
        bot = context.bot
        chatId= update.message.chat_id
        userName = update.effective_user["first_name"]
        logger.info(f"el usuario {userName}  se elimina  marca")

        bot_restart()
        bot.sendMessage(
            chat_id=chatId,
            parse_mode="HTML",
            text= f"Reiniciando Bots recolectores, sistema en linea en 2 minutos"
        )
        
    def web_url(update,context):
        bot = context.bot
        chatId= update.message.chat_id
        userName = update.effective_user["first_name"]
        logger.info(f"el usuario {userName}  edicion Url en la Bd")

        link_mod = context.args[0]
        market = context.args[1]
        try:
            id = context.args[2]
        except: id = None
        try:
         link = context.args[3]
        except: link = None

        if link_mod == "a":
            add_url_db(market, id,link )
            bot.sendMessage(
                chat_id=chatId,
                parse_mode="HTML",
                text= f"se añadio la url a la lista "+id+" del markert "+market+" listas de urls"
                 )  


        if link_mod == "v":
            
            bot.sendMessage(
            chat_id=chatId,
            parse_mode="HTML",
            text= f"El market "+market+" tiene "+ str(urls_per_market(market))
                )  
        
        if link_mod == "c":
            f= view_url( market,id)

            bot = context.bot
            chatId= update.message.chat_id
            bot.sendMessage(
                    chat_id=chatId,
                    parse_mode="HTML",
                    text= f
                )
      
           
    def send_document_price_values(update, context):
        bot = context.bot
        chat_id = update.message.chat_id
        userName = update.effective_user["first_name"]
        logger.info(f"el usuario {userName} ha solicitado una buesqueda")

        market = (context.args[0]).replace("%"," ")
        price_minimo=int(context.args[1])
        price_maximo = int(context.args[2])
     
        try:
         price_maximo = (context.args[2])
        except: price_maximo = None
        bot.sendMessage(
            chat_id=chat_id,
            parse_mode="HTML",
            text= f"Procesado busqueda..."
        )
        search_price(market,price_minimo,price_maximo, bot_token ,chat_id)

        document = open(config("HTML_PATH")+market+".html", 'rb')
        context.bot.send_document(chat_id, document)
        document.close()
        os.remove(config("HTML_PATH")+market+".html")
        print("pasa por aqui")


    ### 14 CREA HTML DE BUSQUEDA DE MARCA Y DSCT PERSONALIZADO
    def fazil_reg(update, context):
        user_id = update.message.from_user.id
        chat_id = update.message.chat_id
        message_text = update.message.text
        userName = update.effective_user["first_name"]
        logger.info(f"el usuario {userName} ha solicitado una buesqueda")
        bot = context.bot
       
        var = message_text
        var = var[2:]
        var = var.split()
     

        if len(var) < 4:
                bot.sendMessage(
            chat_id=chat_id,
            parse_mode="HTML",text= f"Faltan datos para crear la cuenta de fazil "
            #,message_thread_id="5"
             )

        name = (var[0])
        last_name= (var[1])

 
        normalizada = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('utf-8')
        normalizada2 = unicodedata.normalize('NFKD', last_name).encode('ASCII', 'ignore').decode('utf-8')
        if normalizada.isalpha() and normalizada2.isalpha():
            print("La cadena contiene solo letras (sin acentos)")
        else:
           bot.sendMessage(
                chat_id=chat_id,
                parse_mode="HTML",text= f"Formato incorrecto: /f nombre appelido celular email"
                )
           name = None;last_name = None


       
        #dni=str(var[2])
        cel=str(var[2])
        if cel.isdigit() and len(cel) == 9:
            print("The string contains only numbers and 9 digits")
        else:
            bot.sendMessage(
                chat_id=chat_id,
                parse_mode="HTML",text= f"Formato incorrecto: /f nombre appelido celular email, el celular solo debe tener 9 digitos"
                )
            cel = None
            


        email=str(var[3])
        pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

        if re.match(pattern, email):
            print("La dirección de correo electrónico es válida")
        else:
            bot.sendMessage(
                chat_id=chat_id,
                parse_mode="HTML",text= f"Formato incorrecto: /f nombre appelido celular email, formato de email incorrecto"
                )
            email = None
            
        #pwd=str(var[5])
        if name or last_name or cel or email == None:
            print(" error de data input")
        if name and last_name and cel and email != None:
            if user_id == 1160667522 or 1712594729:
                bot.sendMessage(
                    chat_id=chat_id,
                    parse_mode="HTML",text= f"Creando cuenta Fazil"
            
                    )
      
                fazil = register_safa(name,last_name,cel,email)
               

                if fazil == False:
                     bot.sendMessage(
                    chat_id=chat_id,
                    parse_mode="HTML",text= f"El correo ya existe"
                    )
                     
                if fazil == True:
                     bot.sendMessage(
                        chat_id=chat_id,
                        parse_mode="HTML",text= f"Error de Sincronizacion al estilo de Saga falabella, Intenta de nuevo"
                        )
                     
                if fazil =="paso":
                    bot.sendMessage(
                    chat_id=chat_id,
                    parse_mode="HTML",text= f"Acceso Restringido, no estas autorizado a usar este comando"
            

                    )

    def delete_past_database(update, context):
            bot = context.bot
            chatId= update.message.chat_id
            delete_pastdays()
         

            userName = update.effective_user["first_name"]
            logger.info(f"el usuario {userName} ha solicitado informacion sobre el bot " +str(chatId) )
            print(context.args)
            
            bot.sendMessage(
                chat_id=chatId,
                parse_mode="HTML",text= f"Se elimino limpio base de datos❗❗❗ "
          
            )

      
       
    def reset_ship_data(update, context):

        bot = context.bot
        chatId= update.message.chat_id
        collection_data=str(context.args[0])

        reset_products(collection_data)

        bot.sendMessage(
                chat_id=chatId,
                parse_mode="HTML",text= f"Se resteo todo los productos enviados a la nave especificada❗ "
          
            )




    # if __name__ == "__main__":
    myBot = telegram.Bot(token = TOKEN)
    print(myBot.getMe())

    updater = Updater(myBot.token, use_context=True)

    dp= updater.dispatcher
    dp.add_handler(CommandHandler("botinfo", getBotInfo))
    dp.add_handler(CommandHandler("comandos", Commands))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcomeMsg))
    # dp.add_handler(CommandHandler('b', custom_search))
    #dp.add_handler(CommandHandler("url", web_url))
    dp.add_handler(CommandHandler("send", send_document))
    dp.add_handler(CommandHandler("clean", delete_past_database))
    dp.add_handler(CommandHandler("resetship", reset_ship_data))
    dp.add_handler(CommandHandler("price", send_document_price_values))
    dp.add_handler(CommandHandler("product", send_product))
    dp.add_handler(CommandHandler('alert', alert_all))
    # dp.add_handler(CommandHandler('market', custom_search_market))
    dp.add_handler(CommandHandler('cod', sku))
    # dp.add_handler(CommandHandler('auto', auto_tele))
    dp.add_handler(CommandHandler("f", fazil_reg))

    # dp.add_handler(CommandHandler('manual', auto_tele_dsct))
    # dp.add_handler(CommandHandler('restartbot', restart_bot))
    dp.add_handler(CommandHandler('brand', add_brand))
    dp.add_handler(CommandHandler('delete', brand_delete))
    dp.add_handler(CommandHandler('cat', category_list))
    dp.add_handler(CommandHandler('catlist', brand_list))
    dp.add_handler(CommandHandler('marca', brand_to_html))


    updater.start_polling()
    updater.idle()