
import os
import telebot
from PIL import Image

# Initialize the Telegram bot
TOKEN = '6051838838:AAFRoIeuEacgTjD_S0I-aK8CfIXxBvgWvek'
back = "/Users/javier/GIT/fala/demo/back.jpg"
logo2 = "/Users/javier/GIT/fala/demo/image.png"

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

    # Open the base image sent by the user
    base_image = Image.open(photo_path)

    # Calculate the size of the logo image while maintaining the aspect ratio
    logo_size = int(base_image.height * 0.5)
    logo_image = Image.open(logo2)

    # Resize the logo image while maintaining the aspect ratio
    logo_image.thumbnail((logo_size, logo_size))

    # Position the logo image in the top left corner
    logo_position = (0, 0)

    # Create a new image with the same size as the base image
    result = Image.new('RGB', base_image.size)

    # Paste the base image onto the result image
    result.paste(base_image, (0, 0))

    # Paste the logo image onto the result image
    result.paste(logo_image, logo_position, logo_image)

    # Save the final joined image
    result.save('joined_image.jpg')

    # Send the joined image back to the user
    with open('joined_image.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)

    # Remove the temporary files
    os.remove(photo_path)
    os.remove('joined_image.jpg')

# Start the bot
bot.polling()
