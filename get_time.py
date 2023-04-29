# coding: UTF-8
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import datetime


def time_choice():
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

def bcd(txt):#bcdコードに変換
    txt_temp = str(txt)
    if 99 < txt < 1000 : #3桁の場合
        Hundreds_digit  = int(txt_temp[0])
        tens_digit      = int(txt_temp[1])
        ones_digit      = int(txt_temp[2])
    elif 9 < txt < 99:  #2桁の場合
        tens_digit      = int(txt_temp[0])
        ones_digit      = int(txt_temp[1])
    elif 0 < txt < 9 :  #１桁の場合
        nes_digit      = int(txt_temp[0])
    else:
        return 

#変数とオプション
options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--headless')#実際にブラウザを表示しないオプション
options.use_chromium = True
loop_time = 60
retry = 2
#mainloop
time_choice()#時間合わせ
retry_bool = True
while True: 
    while retry_bool:
        for retry_nam in range(1, retry+1):
            driver = webdriver.Chrome(options=options) #ブラウザを起動する
            time.sleep(0)#起動時間待ち
            driver.get("https://napolipizzademae.com/13111056001/1004421")# ブラウザでアクセスする
            time.sleep(0)#処理待ち
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
            print (datetime.datetime.now().strftime("%H:%M:%S"),Take_out_time,delivery_time)
        else:
            print (datetime.datetime.now().strftime("%H:%M:%S")+"can't get time!")

        retry_nam = 1
    time.sleep(loop_time-2)
