from datetime import datetime

def hora():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    date = now.strftime("%d/%m/%Y" )
    print(date)
    return current_time



hora()

