from decouple import config
from bot_unique import super_bot

#TOKEN = "6885697554:AAHLN1UXkMbMnNL-da_PFSLLEY0zpUvcGro" # bug_bug_bot

#chat_id = "-1002046813958"
chat_id = config("TEST1")
bot_token = "6885697554:AAHLN1UXkMbMnNL-da_PFSLLEY0zpUvcGro" 
TOKEN  = "6885697554:AAHLN1UXkMbMnNL-da_PFSLLEY0zpUvcGro" 
db1 = "deep1"
db2 = "deep2"

super_bot(TOKEN, bot_token, chat_id, db1, db2)

