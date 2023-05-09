# coding: UTF-8
import datetime
import logging
import logging.config
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
logging.config.fileConfig('logging.conf')
#mainloop
logging.basicConfig(filename='get_time.log', encoding='utf-8', level=logging.INFO)
logging.info(":START_Program")
lib.time_adjustment.time_adjustment()#時間合わせ
retry_bool = True
while True: 
    while retry_bool:
        for retry_nam in range(1, retry+1):
            lib.time_adjustment.time_adjustment()#時間合わせ
            logging.info("get web source start")
            driver = webdriver.Chrome(options=options) #ブラウザを起動する
            time.sleep(1)#起動時間待ち
            driver.get("https://napolipizzademae.com/13111056001/1004421")# ブラウザでアクセスする
            time.sleep(1)#処理待ち
            html = driver.page_source
            driver.close()#ウェブページを閉じる
            logging.info("web access end")
            driver = None
            soup = BeautifulSoup(html, "html.parser") # BeautifulSoupで扱えるようにパースします
            html = None
            logging.info("html parse")
            txt = soup.text#テキストデータのみ抽出
            logging.info("html to str")
            soup = None
            txt = txt[txt.find("お届け時間")+5:]#以下の２行で時間のみに加工
            txt = txt[:txt.find("分"):]
            logging.info("str processing")
            if txt.isdigit():#整数かどうか判断、整数の場合はループを抜ける                
                retry_bool = True               
                break
            else:
                retry_bool = False
        if retry_bool == True:
            delivery_time = int(txt)
            Take_out_time = (delivery_time/2)-5 #テイクアウト時間算出
            if Take_out_time < 10:#10分以下なら10分に強制書き換え
                Take_out_time = 10
                logging.info("forced rewrite")
            else:
                pass
            logging.info("Take_out_time processing")
            log="Take-out="+str(Take_out_time)+" delivery="+str(delivery_time)
            logging.info(log)
            print (datetime.datetime.now().strftime("%H:%M:%S"),"Take-out ",Take_out_time,"delivery ",delivery_time)
            Sixteen_segment_deta= SSD.str_to_Sixteen_segment_display(str(Take_out_time))
            logging.info("Sixteen_segment_deta processing")
            logging.debug(Sixteen_segment_deta)
        else:

            logging.info (datetime.datetime.now().strftime("%H:%M:%S")+" can't get time!")

        retry_nam = 1
        time.sleep(loop_time-62)
