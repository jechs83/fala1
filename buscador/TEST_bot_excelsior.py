from datetime import datetime
from telegram import ParseMode
from decouple import config
import telegram
import logging
import sys
from telegram import message
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from search_bot_service import busqueda, search_brand_dsct, auto_telegram, auto_telegram_2
from TEST_search_bot_service import add_brand_list, read_brands, auto_search_category, delete_brand,auto_search_category


TOKEN = config("CAPITAN_PIKE_TOKEN")
chat_ide = config("EXCELSIOR_CHAT_TOKEN")
bot_token = config("CAPITAN_PIKE_TOKEN")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s -  %(message)s,")
logger = logging.getLogger()


def getBotInfo(update, context):
    bot = context.bot
    chatId= update.message.chat_id
    userName = update.effective_user["first_name"]
    logger.info(f"el usuario {userName} ha solicitado informacion sobre el bot " +str(chatId))
    print(context.args)
    
    bot.sendMessage(
        chat_id=chatId,
        parse_mode="HTML",
        text= f"Hola soy un bot creado para la Nave Excelsior. sigo funcionando no te preocupes "
    )

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


def custom_search(update, context):
    bot = context.bot
    chatId= update.message.chat_id
    userName = update.effective_user["first_name"]
    logger.info(f"el usuario {userName} ha solicitado una buesqueda")
    brand= (context.args[0]).replace("%"," ")
    dsct=int(context.args[1])
    if dsct <= 41:
       dsct = 40
    search_brand_dsct(brand, dsct, bot_token,chat_ide)

    bot.sendMessage(
        chat_id=chatId,
        parse_mode="HTML",
        text= f"Se realizo busqueda de la marca ingresada "+ str(brand) +" de "+ str(dsct) + "%  a mas\n\n#####################################\n#####################################"
    )


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

### BUSCA PRODUCTO PRO CODIGO DE PRODUCTO ( /cod codigo_deproducto)
def sku(update, context):
    bot = context.bot
    chatId= update.message.chat_id
    userName = update.effective_user["first_name"]
    logger.info(f"el usuario {userName}  busca codigo especifico")
    codigo = context.args[0]
    
    busqueda(str(codigo),bot_token,chat_ide)
    bot.sendMessage(
        chat_id=chatId,
        parse_mode="HTML",
        text= f"Termino la busqueda... si no hay nada no encontre ps"
    )


def auto_tele(update, context):
    bot = context.bot
    chatId= update.message.chat_id
    userName = update.effective_user["first_name"]
    logger.info(f"el usuario {userName}  buscqueda automatica")
    auto_telegram(bot_token,chat_ide,"excelsior1", "excelsior2")
    

def auto_tele2(update, context):
    bot = context.bot
    chatId= update.message.chat_id
    userName = update.effective_user["first_name"]
    logger.info(f"el usuario {userName}  buscqueda automatica")
    auto_telegram_2(bot_token,chat_ide)


    
### EMVIA A TELEGRAM RESULTADO DE LAS MARCAS POR CATEGORIA  ( /auto ropa )
def search_result_brands(update, context):
    bot = context.bot
    chatId= update.message.chat_id
    userName = update.effective_user["first_name"]
    logger.info(f"el usuario {userName}  trata de hacer buscqueda por categoria al 70%")

    category=str(context.args[0])
 
    #send_results_brand_search(category,bot_token,chat_ide)
    bot.sendMessage(
        chat_id=chatId,
        parse_mode="HTML",
        text= f"Por favor espera un momento estoy trabajando en tu solicitud "
    )
    auto_search_category( category,"scrap","excelsior1", "excelsior2" ,bot_token,chat_ide)

    bot.sendMessage(
        chat_id=chatId,
        parse_mode="HTML",
        text= f"Se termino la busqueda.... si no arrojo resultados es porque no hay nada nuevo"
    )


###  ENVIA LISTA DE MARCAS ( /read_brands ropa)
def brands_list(update, context):
    bot = context.bot
    chatId= update.message.chat_id
    userName = update.effective_user["first_name"]
    logger.info(f"el usuario {userName} ha solicitado una buesqueda")
    # brand= str(context.args[0])
    category=context.args[0]
    read_brands(category,bot_token,chat_ide)

### AGREGA MARCA A LA LISTA ( /brand marca ropa)
def add_brand(update, context):
    bot = context.bot
    chatId= update.message.chat_id
    userName = update.effective_user["first_name"]
    logger.info(f"el usuario {userName} ha solicitado una buesqueda")
    brand= (context.args[0]).replace("%"," ")
    
    category=(context.args[1]).replace("%","")
    add_brand_list(brand, category,bot_token,chat_ide)

    bot.sendMessage(
        chat_id=chatId,
        parse_mode="HTML",
        text= f"Se agrego al buscador de "+str(category)+" la "+str(brand)
    )

### ELIMINA MARCA DE LA LISTA (/delete marca ropa)
def brand_delete(update,context):
    bot = context.bot
    chatId= update.message.chat_id
    userName = update.effective_user["first_name"]
    logger.info(f"el usuario {userName}  se elimina  marca")
    brand=(context.args[0]).replace("%","")
    category=context.args[1]

    delete_brand(brand,category,bot_token,chat_ide)


    

if __name__ == "__main__":
    myBot = telegram.Bot(token = TOKEN)
    print(myBot.getMe())

updater = Updater(myBot.token, use_context=True)

dp= updater.dispatcher
dp.add_handler(CommandHandler("botinfo", getBotInfo))
dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcomeMsg))


try:
 dp.add_handler(CommandHandler('b', custom_search))
except:
    print("esta corriendo")


dp.add_handler(CommandHandler('mierdas_compren_rapido', alert_all))

dp.add_handler(CommandHandler('cod', sku))

#dp.add_handler(CommandHandler('auto2', search_result_brands))
dp.add_handler(CommandHandler('auto', search_result_brands))

dp.add_handler(CommandHandler('manual', auto_tele2))

dp.add_handler(CommandHandler('brand', add_brand))
dp.add_handler(CommandHandler('delete', brand_delete))

dp.add_handler(CommandHandler('read_brands', brands_list))

updater.start_polling()
updater.idle()