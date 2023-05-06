# coding: UTF-8
import datetime
import logging
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import lib.Sixteen_segment_display as SSD
import lib.time_adjustment
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
            logging.debug(datetime.datetime.now().strftime("%H:%M:%S"),":get web source start")
            driver = webdriver.Chrome(options=options) #ブラウザを起動する
            time.sleep(1)#起動時間待ち
            driver.get("https://napolipizzademae.com/13111056001/1004421")# ブラウザでアクセスする
            time.sleep(1)#処理待ち
            html = driver.page_source
            driver.close()#ウェブページを閉じる
            logging.debug(datetime.datetime.now().strftime("%H:%M:%S"),":web access end")
            driver = None
            soup = BeautifulSoup(html, "html.parser") # BeautifulSoupで扱えるようにパースします
            html = None
            logging.debug(datetime.datetime.now().strftime("%H:%M:%S"),":html parse")
            txt = soup.text#テキストデータのみ抽出
            logging.debug(datetime.datetime.now().strftime("%H:%M:%S"),":html to str")
            soup = None
            txt = txt[txt.find("お届け時間")+5:]#以下の２行で時間のみに加工
            txt = txt[:txt.find("分"):]
            logging.debug(datetime.datetime.now().strftime("%H:%M:%S"),":str processing")
            if txt.isdigit():#整数かどうか判断、整数の場合はループを抜ける                
                retry_bool = True               
                break
            else:
                retry_bool = False
        if retry_bool == True:
            delivery_time = int(txt)
            Take_out_time = delivery_time-10 #テイクアウト時間算出
            logging.debug(datetime.datetime.now().strftime("%H:%M:%S"),":Take_out_time processing")
            logging.info  (datetime.datetime.now().strftime("%H:%M:%S"),"Take-out ",Take_out_time,"delivery ",delivery_time)
            Sixteen_segment_deta= SSD.str_to_Sixteen_segment_display(str(Take_out_time))
            logging.debug(datetime.datetime.now().strftime("%H:%M:%S"),":Sixteen_segment_deta processing")
            logging.debug(Sixteen_segment_deta)
        else:

            logging.info (datetime.datetime.now().strftime("%H:%M:%S")+" can't get time!")

        retry_nam = 1
        time.sleep(loop_time-62)
