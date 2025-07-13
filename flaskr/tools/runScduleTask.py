import schedule
import time
from schedule import every, repeat

@repeat(every(2).seconds, "every 2 sec")
@repeat(every().day.at("10:30:42"), "every day at 10:30:42")
def hello(planet):
    print('This Annotation job run: ', planet)

def greet(name):
    print('This job run: ', name)

schedule.every(3).seconds.do(greet, name='every 3 sec')
# Run job every minute at the 23rd second
schedule.every().minute.at(":23").do(greet, name='every minute at the 23rd second')
# Run job every hour at the 42rd minute
schedule.every().hour.at(":17").do(greet, name='every hour at the 42rd minute')
# Run job every day at specific HH:MM and next HH:MM:SS
schedule.every().day.at("10:30:42").do(greet, name='every day at 10:30:42')
# If current time is 02:00, first execution is at 06:20:30
schedule.every().wednesday.at("13:15").do(greet, name='every wednesday at 13:15')

try :
    while True :
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt : # control+C press
    pass