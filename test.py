

from datetime import datetime
from datetime import date
import time

def load_datetime():

 today = date.today()
 now = datetime.now()
 date1 = today.strftime("%d/%m/%Y")  
 current_time = now.strftime("%H:%M:%S")
 return current_time, date1


def prueba():
    for i in range (100):
        x = load_datetime()
        print(x[0])
        print(x[1])
        time.sleep(2)
  

prueba()