# coding: UTF-8
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import datetime
import Sixteen_segment_display


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


#変数とオプション
options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--headless')#実際にブラウザを表示しないオプション
options.use_chromium = True
loop_time = 600
retry = 2
#mainloop
time_adjustment()#時間合わせ
retry_bool = True
while True: 
    while retry_bool:
        for retry_nam in range(1, retry+1):
            time_adjustment()#時間合わせ
            driver = webdriver.Chrome(options=options) #ブラウザを起動する
            time.sleep(1)#起動時間待ち
            driver.get("https://napolipizzademae.com/13111056001/1004421")# ブラウザでアクセスする
            time.sleep(1)#処理待ち
            html = driver.page_source
            driver.close()#ウェブページを閉じる
            driver = None
            soup = BeautifulSoup(html, "html.parser") # BeautifulSoupで扱えるようにパースします
            html = None
            txt = soup.text#テキストデータのみ抽出
            soup = None
            txt = txt[txt.find("お届け時間")+5:]#以下の２行で時間のみに加工
            txt = txt[:txt.find("分"):]
            if txt.isdigit():#整数かどうか判断、整数の場合はループを抜ける                
                retry_bool = True               
                break
            else:
                retry_bool = False
        if retry_bool == True:
            delivery_time = int(txt)
            Take_out_time = delivery_time-10 #テイクアウト時間算出
            print (datetime.datetime.now().strftime("%H:%M:%S"),"Take-out ",Take_out_time,"delivery ",delivery_time)
            Sixteen_segment_deta= Sixteen_segment_display.str_to_Sixteen_segment_display(str(Take_out_time))
            print(Sixteen_segment_deta)
        else:
            print (datetime.datetime.now().strftime("%H:%M:%S")+" can't get time!")

        retry_nam = 1
        time.sleep(loop_time-62)
