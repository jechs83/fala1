import sys
import time
import requests
from pymongo import MongoClient
import os
import ast
import re
from datetime import datetime
from telegram import ParseMode
import pytz
from g_var import mongo_db




server_date = datetime.now()

timezone = pytz.timezone("America/Bogota")
peru_date = server_date.astimezone(timezone)
date = peru_date.strftime("%d/%m/%Y" )

time = server_date.strftime("%H:%M" )

h1 = server_date.strftime("4:00")
h2 = server_date.strftime("2:00")

print(date)
print(time)

resta = h1-h2
print(str(resta))