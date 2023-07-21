from decouple import config
from bot_unique_deep import super_bot


TOKEN = config("CAPITAN_PIKE_TOKEN")
chat_id = config("DEEP_CHAT_TOKEN")
bot_token = config("CAPITAN_PIKE_TOKEN")
db1 = "deep1"
db2 = "deep2"

super_bot(TOKEN, bot_token, chat_id, db1, db2)

