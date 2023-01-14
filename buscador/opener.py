import subprocess
import time


def open_python():

    subprocess.call([r'C:\Git\fala\buscador\00.bat'])

    time.sleep(5*60)

    open_python()


open_python()