


import time
import os
import subprocess
from pymongo import MongoClient
from decouple import config
client = MongoClient(config("MONGO_DB"))

def test():
                    

  subprocess.Popen([ "start", "C:\\GIT\\fala\\ripley\\as.py", "100"], shell=True, executable="C:\WINDOWS\system32\cmd.exe")
    subprocess.Popen([ "start", "C:\\GIT\\fala\\ripley\\as.py", "100"], shell=True, executable="C:\WINDOWS\system32\cmd.exe")
      