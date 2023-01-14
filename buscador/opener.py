import subprocess
import time


def open_python():

    subprocess.call([r'/Users/javier/GIT/fala/buscador/1.bat'])


    time.sleep(60)

    open_python()


open_python()