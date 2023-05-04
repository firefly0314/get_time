import datetime
import time


def time_adjustment():
    sleep_sec=datetime.datetime.now().time() 
    return sleep_sec


time_difference=time_adjustment
print(time_difference)