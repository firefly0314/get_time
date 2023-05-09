import datetime 
import time
import logging

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
    mini=mini*60
    time_now = ((datetime.datetime.now().minute)*60)+((datetime.datetime.now().second))
    Next_time=-(-time_now // mini) * mini
    sleep_sec = (Next_time)-(time_now)
    log="sleep_sec "+str(sleep_sec)
    logging.info(log)
    time.sleep(sleep_sec)