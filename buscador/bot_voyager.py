
from decouple import config
from bot_unique import super_bot


TOKEN = config("CAPITAN_JANEWAY_TOKEN")
chat_id = config("VOYAGER_CHAT_TOKEN")
bot_token = config("CAPITAN_JANEWAY_TOKEN")
db1 = "voyager1"
db2 = "voyager2"


super_bot(TOKEN, bot_token, chat_id, db1, db2)

