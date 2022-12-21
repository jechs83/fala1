from decouple import config
from bot_unique import super_bot


TOKEN = config("CAPITAN_PIKE_TOKEN")
chat_id = config("EXCELSIOR_CHAT_TOKEN")
bot_token = config("CAPITAN_PIKE_TOKEN")

super_bot(TOKEN, bot_token, chat_id)

