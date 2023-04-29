import datetime
import time
time_bool = False


while not time_bool:
    time_now = datetime.datetime.now().minute
    #time_now = 20
    print(time_now)
    if -1 < time_now < 60:
        for i in range(0,60,10):
            time_division_remainder = (time_now+10)%(i+10)
            if time_division_remainder == 0:
                time_bool = True
                break
            else:
                time_bool = False
                time.sleep(1)
        
                


print(time_bool)