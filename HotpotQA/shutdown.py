import time
import os
from time import sleep

judge = True
while judge:
    t = time.localtime()
    day = t.tm_mday
    hour = t.tm_hour
    minute = t.tm_min
    second = t.tm_sec
    print(day)
    if hour >= 0 and day > 19:
        os.system("shutdown -s -t 10 ")
        judge = False
    else:
        print(hour, minute, second)
        print("还没到点")
    sleep(1800)