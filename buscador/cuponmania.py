
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
import pytesseract
from PIL import Image

# Reemplaza 'TU_TOKEN' con el token que te proporcionó BotFather
TOKEN = '6794925800:AAExqiVDl3UeGEopEhRMAqDPrqQYF6M_1bg'

# ID del chat al que quieres reenviar la foto y el mensaje
DESTINATION_CHAT_ID = '-1002046813958'

# Lista de IDs de usuarios permitidos
USERS_ALLOWED = [1160667522,1499144180,1712594729]  # Reemplaza con los IDs de usuarios permitidos
# spock, fasky, irvin, ruth

def photo_handler(update: Update, context: CallbackContext):
    # Obtener la foto enviada
    photo = update.message.photo[-1].file_id
    
    # Obtener el chat ID de donde se envió la foto
    chat_id = update.message.chat_id
    # Obtener información adicional si es necesaria
    caption = update.message.caption

    # Verificar si el ID del remitente está en la lista de IDs permitidos
    if update.message.from_user.id in USERS_ALLOWED:
        # Crear el objeto bot
        bot = context.bot

        # Obtener la información de la foto original
        photo_info = update.message.photo[-1].get_file()

        # Descargar la foto
        new_photo = photo_info.download()

        # Enviar la foto con un nuevo mensaje
        bot.send_photo(chat_id=DESTINATION_CHAT_ID, photo=open(new_photo, 'rb'), caption=caption)

def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Manejar la recepción de fotos
    dispatcher.add_handler(MessageHandler(Filters.photo, photo_handler))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()