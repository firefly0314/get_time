# coding: UTF-8
import datetime
import logging
import logging.config
import time
import tomllib

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
loop_time = 10
retry = 2
logging.config.fileConfig('logging.conf')

#tomlから変更点を書き込み
with open('mein_setting.toml', 'rb') as f:
    settings = tomllib.load(f)

loop_time = settings["loop_time"]
retry = settings["web_get_retry"]
URL = settings["napoli_URL"]
#mainloop
logging.basicConfig(filename='get_time.log', encoding='utf-8', level=logging.INFO)
logging.info(":START_Program")
retry_bool = True
txt=""
retry_nam = 1
while True: 
    #lib.time_adjustment.time_adjustmentV2(loop_time)#時間合わせ
    while retry_bool:
                   
        logging.info("get web source start")
        driver = webdriver.Chrome(options=options) #ブラウザを起動する
        #time.sleep(1)#起動時間待ち
        #driver.get(URL)# ブラウザでアクセスする
        #time.sleep(1)#処理待ち
        html = driver.page_source
        driver.close()#ウェブページを閉じる
        logging.info("web access end")
        soup = BeautifulSoup(html, "html.parser") # BeautifulSoupで扱えるようにパースします        
        logging.info("html parse")
        txt = soup.text#テキストデータのみ抽出
        logging.info("html to str")         
        logging.info("str processing")
        txt = txt[txt.find("お届け時間")+5:]#以下の２行で時間のみに加工
        txt = txt[:txt.find("分"):]

        if txt.isdigit():#整数かどうか判断、整数の場合はループを抜ける                
            retry_bool = False
            print_bool = True
            logging.info("html check OK")                  
        else:
            retry_bool = True
            logging.warning("html check NG retry")
        if retry_nam == retry:
            logging.info ("can't get time!")
            retry_bool = False
            print_bool = False
            retry_nam = 1
        elif retry_nam < retry:
            retry_nam = retry_nam+1
            retry_bool = True
            
        soup = None
        html = None
        driver = None
        
    #ここからが数値処理

    if print_bool == True:
        logging.info("Take_out_time processing")
        delivery_time = int(txt)
        Take_out_time = int((delivery_time/2)-5) #テイクアウト時間算出
        if Take_out_time < 10:#10分以下なら10分に強制書き換え
            Take_out_time = 10
            logging.info("forced rewrite")
        else:
            logging.info("not rewrite")
        logging.info("Take-out="+str(Take_out_time)+" delivery="+str(delivery_time))
        print (datetime.datetime.now().strftime("%H:%M:%S"),"Take-out ",Take_out_time,"delivery ",delivery_time)
        Sixteen_segment_deta= SSD.str_to_Sixteen_segment_display(str(Take_out_time))
        logging.info("Sixteen_segment_deta processing")
        logging.debug(Sixteen_segment_deta)
        print_bool=False
    else:
        logging.info ("can't get time!")
        
    retry_bool = True
