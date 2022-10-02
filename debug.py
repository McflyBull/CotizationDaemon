from datetime import datetime
from time import gmtime, strftime

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)
print("Your Time Zone is GMT", strftime("%z", gmtime()))