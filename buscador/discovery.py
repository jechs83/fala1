

from decouple import config
from bot_unique import super_bot




TOKEN = config("CAPITAN_SPOK_TOKEN")
chat_id = config("DISCOVERY_CHAT_TOKEN")
bot_token = config("CAPITAN_SPOK_TOKEN")


super_bot(TOKEN, bot_token, chat_id)
