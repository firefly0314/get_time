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

def bcd(txt):
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
        print(datetime.datetime.now(),":value error")

#変数とオプション
options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--headless')#実際にブラウザを表示しないオプション
options.use_chromium = True
loop_time = 60
retry = 3

time_choice()
time_bool = False
while True: 
    while not time_bool:
        for retry_nam in range(0, retry):
            driver = webdriver.Chrome(options=options) #ブラウザを起動する
            time.sleep(1)#起動時間待ち
            driver.get("https://napolipizzademae.com/13111056001/1004421")# ブラウザでアクセスする
            time.sleep(1)#処理待ち
            html = driver.page_source
            driver.close()#ウェブページを閉じる
            soup = BeautifulSoup(html, "html.parser") # BeautifulSoupで扱えるようにパースします

            txt = soup.text#テキストデータのみ抽出
            txt = txt[txt.find("お届け時間")+5:]#以下の２行で時間のみに加工
            txt = txt[:txt.find("分"):]

            if txt.isdigit():#整数かどうか判断
                txt = int(txt)
                txt = txt-10 #テイクアウト時間算出
                print (datetime.datetime.now(),txt)
                #bcdコードに変換
                txt_temp = str(txt)
                retry_bool = True
                if 99 < txt < 1000 : #3桁の場合
                    Hundreds_digit  = int(txt_temp[0])
                    tens_digit      = int(txt_temp[1])
                    ones_digit      = int(txt_temp[2])
                elif 9 < txt < 99:  #2桁の場合
                    tens_digit      = int(txt_temp[0])
                    ones_digit      = int(txt_temp[1])
                elif 0 < txt < 9 :  #１桁の場合
                    ones_digit      = int(txt_temp[0])
            else:
                print(datetime.datetime.now(),":value error")
                retry_bool = False
            retry_nam = 0
            break
    time.sleep(loop_time-2)
