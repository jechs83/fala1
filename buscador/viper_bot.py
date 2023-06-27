

from decouple import config
from bot_unique import super_bot


TOKEN = "6201012907:AAEJQ_4sauVNRgbusNvGc4q2_Ijk6nsVwX0"
chat_id = config("NAME_LESS_TOKEN")
#chat_id = config("DISCOVERY_50_100")

bot_token = "6201012907:AAEJQ_4sauVNRgbusNvGc4q2_Ijk6nsVwX0"
db1 = "viper1"
db2 = "viper2"
super_bot(TOKEN, bot_token, chat_id, db1, db2)

