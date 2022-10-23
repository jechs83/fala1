
from datetime import datetime
from telegram import ParseMode
import telegram
import logging
from telegram import message
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram_busca import busqueda , brand_search
date = datetime.today().strftime('%d-%m-%Y')
date_now = datetime.today().strftime('%d-%m-%Y')
TOKEN = "5504401191:AAG8Wuk5AF95qEWn0642ZjhzduE0CbVkBaU"

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s -  %(message)s,"
)
logger = logging.getLogger()


def getBotInfo(update, context):
    bot = context.bot
    chatId= update.message.chat_id
    userName = update.effective_user["first_name"]
    logger.info(f"el usuario {userName} ha solicitado informacion sobre el bot")
    bot.sendMessage(
        chat_id=chatId,
        parse_mode="HTML",
        text= f"Hola soy un bot creado para el canal de Enterprice"
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

def echo(update, context):
    bot = context.bot
    chatId = update.message.chat_id
    text = update.message.text
    logger.info(f"El usuario a enviado un nuevo mensaje al grupo {chatId} ")

    if "cod:"  in text:
        print(text)
        codigo = text.replace("cod:","")
        busqueda(codigo)
    
    if "Cod:"  in text:
        print(text)
        codigo = text.replace("Cod:","")
        busqueda(codigo)


    if "brand:"  in text:
        print(text)
        brand = text.replace("brand:","")
        brand_search(brand)

        bot = context.bot
        chatId= update.message.chat_id
        userName = update.effective_user["first_name"]
        bot.sendMessage(
        chat_id= chatId,
        parse_mode= "HTML",
        text=f"Ya no hay mas, No Jodas {userName}."
             )

    
    if "Brand:"  in text:
        print(text)
        brand = text.replace("Brand:","")
        brand_search(brand)

        bot = context.bot
        chatId= update.message.chat_id
        userName = update.effective_user["first_name"]
        bot.sendMessage(
        chat_id= chatId,
        parse_mode= "HTML",
        text=f"Ya no hay mas, No Jodas {userName}."
             )

    



if __name__ == "__main__":
    myBot = telegram.Bot(token = TOKEN)
    print(myBot.getMe())

updater = Updater(myBot.token, use_context=True)



dp= updater.dispatcher
dp.add_handler(CommandHandler("botInfo", getBotInfo))
dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcomeMsg))
dp.add_handler(MessageHandler( Filters.text, echo))
updater.start_polling()
updater.idle()