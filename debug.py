from datetime import datetime
from time import gmtime, strftime

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)
print("Your Time Zone is GMT", strftime("%z", gmtime()))


import pytz  # 3rd party: $ pip install pytz








dayNow = int(now.strftime("%d"))
hourNow = int(now.strftime("%H"))

print(dayNow)
print(hourNow)
