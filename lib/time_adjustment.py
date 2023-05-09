import datetime 
import time

def time_adjustment():
    time_bool = False
    while not time_bool:
        time_now = datetime.datetime.now().minute
        if -1 < time_now < 60:
            for i in range(0,60,10):
                time_division_remainder = (time_now+10)%(i+10)
                if time_division_remainder == 0:
                    time_bool = True
                    break
                else:
                    time_bool = False
                    time.sleep(1)
    return

def time_adjustmentV2(mini):
    time_now = datetime.datetime.now().minute
    Next_time=-(-time_now // mini) * mini
    print(Next_time)
    sleep_sec = (Next_time*60)-(time_now*60)
    print(sleep_sec)
    time.sleep(sleep_sec)