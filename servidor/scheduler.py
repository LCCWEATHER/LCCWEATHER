import schedule
import time
from update import update

schedule.every(30).seconds.do(update)

while True:
    schedule.run_pending()
    time.sleep(1)
