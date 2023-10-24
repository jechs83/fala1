from decouple import config
from bot_unique_deep import super_bot

TOKEN = config("VIPER_TOKEN")
chat_id = config("VIPER_CHAT")
bot_token = config("VIPER_TOKEN")
db1 = "deep1"
db2 = "deep2"

super_bot(TOKEN, bot_token, chat_id, db1, db2)

