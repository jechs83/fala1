from decouple import config
from bot_unique import super_bot


TOKEN = config("RICHI_BOY_TOKEN")
chat_id = config("RICHI_CHAT_TOKEN")
bot_token = config("RICHI_BOY_TOKEN")
db1 = "richi1"
db2 = "richi2"
super_bot(TOKEN, bot_token, chat_id, db1, db2)

