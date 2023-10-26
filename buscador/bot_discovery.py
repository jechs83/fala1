

from decouple import config
from bot_unique import super_bot

TOKEN = config("DISCOVERY_TOKEN")
chat_id = config("DISCOVERY_CHAT")
bot_token = config("DISCOVERY_TOKEN")
db1 = "discovery1"
db2 = "discovery2"

super_bot(TOKEN, bot_token, chat_id, db1, db2)