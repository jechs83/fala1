
from datetime import datetime
import pytz
server_date = datetime.now()
timezone = pytz.timezone("America/Bogota")
peru_date = server_date.astimezone(timezone)
curren_day = peru_date.strftime("%d/%m/%Y" )
current_time =peru_date.strftime("%H:%M" )

print(curren_day)
print(current_time)
