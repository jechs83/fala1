from decouple import config
import telegram
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from register import     register_safa
from search_bot_service import busqueda, search_brand_dsct, auto_telegram, delete_brand,add_brand_list,read_category,manual_telegram, search_market_dsct,search_market2_dsct, search_product_dsct_html, test2, search_brand_dsct_html,read_brands,search_market_dsct_antitopo


def super_bot(TOKEN, bot_token ,chat_id, db1,db2):

    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s -  %(message)s,")
    logger = logging.getLogger()

### 1 ENVIA EL STATUS DEL BOT 
    def getBotInfo(update, context):
        bot = context.bot
        user_id = update.message.from_user.id
        chatId= update.message.chat_id
        userName = update.effective_user["first_name"]
   
        logger.info(f"el usuario {userName} ha solicitado informacion sobre el bot " +str(chatId) +" "+str(user_id))
        print(context.args)
        
        bot.sendMessage(
            chat_id=chatId,
            parse_mode="HTML",
            #parse_mode="MarkdownV2",
            text= f"Hola soy un bot creado para la Nave por Sr Spok. sigo funcionando no te preocupes "
        
        )

    def find_pack(update, context):
        bot = context.bot
        user_id = update.message.from_user.id
        chatId= update.message.chat_id
        userName = update.effective_user["first_name"]
   
        logger.info(f"el usuario {userName} ha solicitado informacion sobre el bot " +str(chatId) +" "+str(user_id))
        print(context.args)
        person= (context.args[0]).replace("%"," ")
        bot.sendMessage(
            chat_id=chatId,
            parse_mode="HTML",
            #parse_mode="MarkdownV2",
            text= f"Espere un momento... buscando el pack de "+person
        
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
            text=f"Bienvenido al grupo {userName}.\n\n REGLAS DE LA NAVE\n1. Compartir las ofertas solamente al grupo de Ofertas Peru\n2. Si hay alguna oferta interesante cominucarlo al Administrador.\n3. No sean casa solas avisen y compren una unidad para todos los del grupo puedan comoprar tambien"
        )

### 4 BUSCA EN BASE A MARCA Y DESCUENTO 
    def custom_search(update, context):
        bot = context.bot
        chatId= update.message.chat_id
        userName = update.effective_user["first_name"]
        logger.info(f"el usuario {userName} ha solicitado una buesqueda")
        brand= (context.args[0]).replace("%"," ")
        dsct=int(context.args[1])
        if dsct <= 41:
           dsct = 40
        search_brand_dsct(brand, dsct, bot_token ,chat_id)

        bot.sendMessage(
            chat_id=chatId,
            parse_mode="HTML",
            text= f"Se realizo busqueda de la marca ingresada "+ str(brand) +" de "+ str(dsct) + "%  a mas\n\n#####################################\n#####################################"
        )

### 5 BUSCA EN BASE A MARKET Y DESCUENTO
    def custom_search_market(update, context):
        bot = context.bot
        user_id = update.message.from_user.id
        chatId= update.message.chat_id
        userName = update.effective_user["first_name"]
        logger.info(f"el usuario {userName} ha solicitado una buesqueda")
        
        if user_id == 1160667522:

            market= (context.args[0]).replace("%"," ")
            dsct=int(context.args[1])
            try:
                dsct2 = int(context.args[2])
            except: dsct2 = None

            if dsct2 ==None:
                
                dsct = int(dsct)
                if dsct <= 41:
                    dsct = 40
                
                search_market_dsct(str(market), int(dsct), bot_token ,chat_id)

                logger.info(f"marca "+ market + "dsct "+ str(dsct))

                bot.sendMessage(
                    chat_id=chatId,
                    parse_mode="HTML",
                    text= f"Se realizo busqueda de la marca ingresada"+ str(market) +" de "+ str(dsct) + "%  a mas\n\n#####################################\n#####################################"
                     )
                
            else:
                 search_market_dsct_antitopo(str(market), int(dsct),int(dsct2), bot_token ,chat_id)

        else:
              bot.sendMessage(
                chat_id=chatId,
                parse_mode="HTML",
                text= f"NO ESTAS AUTORIZADO PARA USAR LA NAVE TOPO"
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
        
        auto_telegram( category,db1, db2 ,bot_token ,chat_id)

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
        chat_id = update.message.chat_id
        userName = update.effective_user["first_name"]
        logger.info(f"el usuario {userName} ha solicitado una buesqueda")

        market = (context.args[0]).replace("%"," ")
        dsct=int(context.args[1])
        dsct = int(dsct)
     
        try:
         price = (context.args[2])
        except: price = None

        search_market2_dsct(market,dsct,price, bot_token ,chat_id)

        document = open(config("HTML_PATH")+market+".html", 'rb')
        context.bot.send_document(chat_id, document)
        document.close()
        os.remove(config("HTML_PATH")+market+".html")
        print("pasa por aqui")
       
      
        
### 14 CREA HTML DE BUSQUEDA DE PALABRA CONTENIDA EN EL NOMBRE DEL PRODUCTO Y DSCT PERSONALIZADO POSIBLE ORDENAR PRECIO MAYOR A MENOR
    def send_product(update, context):
        chat_id = update.message.chat_id
        userName = update.effective_user["first_name"]
        logger.info(f"el usuario {userName} ha solicitado una buesqueda")

        product = (context.args[0]).replace("%"," ")
        dsct=int(context.args[1])
    
        try:
         price = (context.args[2])
        except: price = None
        

        search_product_dsct_html(product,dsct,price ,bot_token ,chat_id)

        document = open(config("HTML_PATH")+"producto.html", 'rb')
        context.bot.send_document(chat_id, document)
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
        
        
    def rules(update, context):
            bot = context.bot
            chatId= update.message.chat_id
            userName = update.effective_user["first_name"]
            logger.info(f"el usuario {userName} pidio las  reglas de la nave")
            
            bot.sendMessage(
            chat_id=chatId,
            parse_mode="HTML",
                        text=f"REGLAS DE LA NAVE\n\n1. Compartir las ofertas solamente al grupo de Ofertas Peru\n2. Si hay alguna oferta interesante cominucarlo al Administrador.\n3. No sean casa solas avisen y compren una unidad para todos los del grupo puedan comoprar tambien"
        )
        
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
        #dni=str(var[2])
        cel=str(var[2])
        email=str(var[3])
        #pwd=str(var[5])

        if user_id == 1160667522 or 1712594729:
            bot.sendMessage(
                chat_id=chat_id,
                parse_mode="HTML",text= f"Creando cuenta Fazil"
        
                )
            try:
                register_safa(name,last_name,cel,email)
                bot.sendMessage(
                chat_id=chat_id,
                parse_mode="HTML",text= f"Usuario se creo exitosamente "
                )
            except:
    
        
                bot.sendMessage(
                chat_id=chat_id,
                parse_mode="HTML",text= f"Usuario ya existe o hubo error en el proceso "
        
                )
        else:
            bot.sendMessage(
                chat_id=chat_id,
                parse_mode="HTML",text= f"Acceso Restringido, no estas autorizado a usar este comando"
        
                )


      
       


        

    # if __name__ == "__main__":
    myBot = telegram.Bot(token = TOKEN)
    print(myBot.getMe())

    updater = Updater(myBot.token, use_context=True)

    dp= updater.dispatcher
    dp.add_handler(CommandHandler("botinfo", getBotInfo))
    dp.add_handler(CommandHandler("pack", find_pack))
    dp.add_handler(CommandHandler('market', custom_search_market))
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcomeMsg))
    dp.add_handler(CommandHandler('cod', sku))
    dp.add_handler(CommandHandler('rules', rules))
    dp.add_handler(CommandHandler("topo", fazil_reg))
 

    updater.start_polling()
    updater.idle()