

from decouple import config
from bot_unique2 import super_bot

TOKEN = config("CAPITAN_KIRK_TOKEN")
chat_id = config("ENTERPRISE_CHAT_TOKEN")
bot_token = config("CAPITAN_KIRK_TOKEN")
db1 = "enterprise1"
db2 = "enterprise2"

super_bot(TOKEN, bot_token, chat_id,db1,db2)

