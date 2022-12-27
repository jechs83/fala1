

from decouple import config
from bot_unique import super_bot




TOKEN = config("CAPITAN_SPOK_TOKEN")
chat_id = config("DISCOVERY_CHAT_TOKEN")
bot_token = config("CAPITAN_SPOK_TOKEN")


db1 = "discovery1"
db2 = "discovery2"
super_bot(TOKEN, bot_token, chat_id, db1, db2)