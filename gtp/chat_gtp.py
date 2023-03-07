import openai
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Set up the OpenAI API key
openai.api_key = "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"

# Define the function to handle incoming messages
def message_handler(update, context):
    # Get the message text
    message_text = update.message.text
    
    # Generate a response using the ChatGPT API
    response = openai.Completion.create(
        engine="davinci",
        prompt=message_text,
        temperature=0.5,
        max_tokens=1024,
        n=1,
        stop=None,
        timeout=60,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    # Get the response text
    response_text = response.choices[0].text.strip()
    
    # Send the response back to the user
    context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)

# Set up the Telegram bot
updater = Updater(token="6169487266:AAGfzV9_y38T29Mrj_RgsT69lDf4_kVzATw", use_context=True)
dispatcher = updater.dispatcher

# Set up the message handler
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))

# Start the bot
updater.start_polling()
