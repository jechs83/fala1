from datetime import datetime
from telegram import ParseMode
from decouple import config
import telegram
import logging
import sys
from telegram import message
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from search_bot_service import busqueda, search_brand_dsct, auto_telegram, delete_brand,add_brand_list,read_brands,manual_telegram, search_market_dsct,search_market2_dsct, search_product_dsct_html

from bot_functios import *
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


def custom_search_market(update, context):
    bot = context.bot
    chatId= update.message.chat_id
    userName = update.effective_user["first_name"]
    logger.info(f"el usuario {userName} ha solicitado una buesqueda")
    market= (context.args[0]).replace("%"," ")
    dsct=int(context.args[1])
    dsct = int(dsct)
    if dsct <= 41:
       dsct = 40
       
    search_market_dsct(str(market), int(dsct),bot_token,chat_ide)

    logger.info(f"marca "+ market + "dsct "+ str(dsct))

    bot.sendMessage(
        chat_id=chatId,
        parse_mode="HTML",
        text= f"Se realizo busqueda de la marca ingresada"+ str(market) +" de "+ str(dsct) + "%  a mas\n\n#####################################\n#####################################"
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
    logger.info(f"el usuario {userName}  busqueda automatica")
    category=str(context.args[0])
    bot.sendMessage(
        chat_id=chatId,
        parse_mode="HTML",
        text= f"Espera un momento se esta procesando la solicitud "
    )
    
    auto_telegram( category,"scrap","excelsior1", "excelsior2" ,bot_token,chat_ide)

    bot.sendMessage(
        chat_id=chatId,
        parse_mode="HTML",
        text= f"Se termino la busqueda "
    )
    logger.info(f"se Termino la Busqueda")
    



###########################################################################

###  ENVIA LISTA DE MARCAS ( /read_brands ropa)
def brands_list(update, context):
    bot = context.bot
    chatId= update.message.chat_id
    userName = update.effective_user["first_name"]
    logger.info(f"el usuario {userName} ha solicitado una buesqueda")
   
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
    
    manual_telegram( category,dsct ,bot_token,chat_ide)

    bot.sendMessage(
        chat_id=chatId,
        parse_mode="HTML",
        text= f"Se termino la busqueda "
    )
    logger.info(f"se Termino la Busqueda")








def send_document(update, context):
    chat_id = update.message.chat_id
    userName = update.effective_user["first_name"]
    logger.info(f"el usuario {userName} ha solicitado una buesqueda")

    market = (context.args[0]).replace("%"," ")
    dsct=int(context.args[1])
    dsct = int(dsct)

    search_market2_dsct(market,dsct, bot_token, chat_ide)

    document = open("C:\\Git\\fala\\buscador\\"+market+".html", 'rb')
    context.bot.send_document(chat_id, document)


def send_product(update, context):
    chat_id = update.message.chat_id
    userName = update.effective_user["first_name"]
    logger.info(f"el usuario {userName} ha solicitado una buesqueda")

    product = (context.args[0]).replace("%"," ")
    dsct=int(context.args[1])
   
    
    search_product_dsct_html(product,dsct, bot_token, chat_ide)

    document = open("C:\\Git\\fala\\buscador\\producto.html", 'rb')
    context.bot.send_document(chat_id, document)








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

dp.add_handler(CommandHandler("send", send_document))

dp.add_handler(CommandHandler("product", send_product))
dp.add_handler(CommandHandler('alert', alert_all))

dp.add_handler(CommandHandler('market', custom_search_market))
dp.add_handler(CommandHandler('cod', sku))

dp.add_handler(CommandHandler('auto', auto_tele))

dp.add_handler(CommandHandler('manual', auto_tele_dsct))

###############################

dp.add_handler(CommandHandler('brand', add_brand))
dp.add_handler(CommandHandler('delete', brand_delete))
dp.add_handler(CommandHandler('cat', brands_list))

updater.start_polling()
updater.idle()