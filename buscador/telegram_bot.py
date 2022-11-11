from datetime import datetime
from telegram import ParseMode
from decouple import config
import telegram
import logging
import sys
from telegram import message
from auto_telegram import auto_telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram_busca import busqueda, search_brand_dsct
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
    if dsct <= 41:
       dsct = 40
    search_brand_dsct(brand, dsct)

    bot.sendMessage(
        chat_id=chatId,
        parse_mode="HTML",
        text= f"Se realizo busqueda de la marca "+ brand +" de "+ dsct + " a mas\n\n#####################################\n#####################################""
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



def auto_search(update, context):
    bot = context.bot
    chatId= update.message.chat_id
    userName = update.effective_user["first_name"]
    logger.info(f"el usuario {userName} ha solicitado una buesqueda")
  
    auto_telegram()

    bot.sendMessage(
        chat_id=chatId,
        parse_mode="HTML",
        text= f"Se realizo busqueda de marcas seleccionadasde 70%  a mas \n\n#################################."
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
dp.add_handler(CommandHandler('auto', auto_search))

dp.add_handler(CommandHandler('mierdas_compren_rapido', alert_all))

dp.add_handler(CommandHandler('cod', sku))






updater.start_polling()
updater.idle()