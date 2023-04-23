from restart_bot import close, restart

import time


def start():
   
    restart()
    time.sleep(30*60)
    start()


start()
    