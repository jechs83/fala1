
from datetime import datetime
from telegram import ParseMode
from decouple import config
import telegram
import logging
import sys
from telegram import message
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram_busca import busqueda , brand_search, search_brand_dsct, product_search, price_search
date = datetime.today().strftime('%d-%m-%Y')
date_now = datetime.today().strftime('%d-%m-%Y')
TOKEN = config("TOKEN_CHAT")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s -  %(message)s,"
)
logger = logging.getLogger()


def getBotInfo(update, context):
    bot = context.bot
    chatId= update.message.chat_id
    userName = update.effective_user["first_name"]
    logger.info(f"el usuario {userName} ha solicitado informacion sobre el bot")
    print(context.args)
    bot.sendMessage(
        chat_id=chatId,
        parse_mode="HTML",
        text= f"Hola soy un bot creado para la Nave de Discovery"
    )

def welcomeMsg(update, context):
    bot = context.bot
    chatId = update.message.chat_id
    updateMsg= getattr(update, "message", None)
    for user in updateMsg.new_chat_members:
        userName = user.first_name
    
    logger.info(f"El usuario {userName} ha ingresado al grupo")

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
    brand= str(context.args[0])
    dsct=int(context.args[1])
    if dsct < 41:
       dsct = 40
    search_brand_dsct(brand, dsct)

    bot.sendMessage(
        chat_id=chatId,
        parse_mode="HTML",
        text= f"Ya no se encontro nada Recon.. ahora si que pase el siguiente gil con su busqueda PTM\n#################################\n CarLitux  deja de buscar tus consoladores y huevadas......."
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
    
    busqueda(str(codigo))
    bot.sendMessage(
        chat_id=chatId,
        parse_mode="HTML",
        text= f"Termino la busqueda... si no hay nada no encontre ps"
    )

def producto(update, context):
    bot = context.bot
    chatId= update.message.chat_id
    userName = update.effective_user["first_name"]
    logger.info(f"el usuario {userName}  busca poducto especifico")
    producto = str(context.args[0])
    dsct = int(context.args[1])
    if dsct < 31:
           dsct = 30

    product_search(producto,dsct)

    bot.sendMessage(
        chat_id=chatId,
        parse_mode="HTML",
        text= f"Termino la busqueda... si no hay nada no encontre ps"
    )

def price_max(update, context):
    bot = context.bot
    chatId= update.message.chat_id
    userName = update.effective_user["first_name"]
    logger.info(f"el usuario {userName}  busca poducto especifico")
    producto = str(context.args[0])
    price = float(context.args[1])
    print(price)

    price_search(producto,price)

    bot.sendMessage(
        chat_id=chatId,
        parse_mode="HTML",
        text= f"Termino la busqueda... si no hay nada no encontre ps"
    )


    def one_brand(update, context):
        bot = context.bot
    chatId= update.message.chat_id
    userName = update.effective_user["first_name"]
    logger.info(f"el usuario {userName}  busca poducto especifico")
    producto = str(context.args[0])
    dsct = int(context.args[1])
    if dsct < 31:
           dsct = 30

    product_search(producto,dsct)

    bot.sendMessage(
        chat_id=chatId,
        parse_mode="HTML",
        text= f"Termino la busqueda... si no hay nada no encontre ps"
    )

    


if __name__ == "__main__":
    myBot = telegram.Bot(token = TOKEN)
    print(myBot.getMe())

updater = Updater(myBot.token, use_context=True)



dp= updater.dispatcher
dp.add_handler(CommandHandler("botInfo", getBotInfo))
dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcomeMsg))

#dp.add_handler(MessageHandler( Filters.text, echo))
try:
 dp.add_handler(CommandHandler('buscar', custom_search))
except:
    print("esta corriendo")

dp.add_handler(CommandHandler('mierdas_compren_rapido', alert_all))
dp.add_handler(CommandHandler('product', producto))
dp.add_handler(CommandHandler('cod', sku))
dp.add_handler(CommandHandler('price', price_search))





updater.start_polling()
updater.idle()