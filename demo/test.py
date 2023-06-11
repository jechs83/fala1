
import os
import telebot
from PIL import Image

# Initialize the Telegram bot
TOKEN = '6051838838:AAFRoIeuEacgTjD_S0I-aK8CfIXxBvgWvek'
back = "/Users/javier/GIT/fala/demo/back.jpg"
logo2 = "/Users/javier/GIT/fala/demo/image.png"

import os
import telebot
from PIL import Image

# Initialize the Telegram bot
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # Get the photo sent by the user
    photo_id = message.photo[-1].file_id
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Save the downloaded photo locally
    photo_path = 'photo.jpg'
    with open(photo_path, 'wb') as photo:
        photo.write(downloaded_file)

    # Open the three images
    background = Image.open(photo_path)
    middle = Image.open(logo2)
    #logo = Image.open(logo2)

    # Resize the middle image to fit the background
    #middle = middle.resize(background.size)

    # Create a new image with the background as base
    result = Image.new('RGBA', background.size)

    # Paste the background onto the result image
    result.paste(background, (0, 0))

    # Create a mask from the alpha channel of the middle image
    #mask = middle.split()[2]  # Assuming the alpha channel is the fourth channel (index 3)

    # Paste the middle image onto the result image using the mask
    #result.paste(middle, (0, 0), mask=mask)

    # Paste the logo on top
    #result.paste(logo, (0, 0), logo)

    # Save the final joined image in PNG format
    result.save('joined_image.png')

    # Send the joined image back to the user
    with open('joined_image.png', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)

    # Remove the temporary files
    os.remove(photo_path)
    os.remove('joined_image.png')

# Start the bot
bot.polling()
