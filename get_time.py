# coding: UTF-8
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--headless')
options.use_chromium = True
loop_time = 600

while True: 
    # ブラウザを起動する
    driver = webdriver.Chrome(chrome_options=options)
    time.sleep(1)
    # ブラウザでアクセスする
    driver.get("https://napolipizzademae.com/13111056001/1004421")
    time.sleep(1)
    html = driver.page_source
    driver.close()
    # BeautifulSoupで扱えるようにパースします
    soup = BeautifulSoup(html, "html.parser")

    txt = soup.text
    txt = txt[txt.find("お届け時間")+5:]
    txt = txt[:txt.find("分"):]
    txt = int(txt)

    txt = txt-10 #テイクアウト時間算出

    #bcdコードに変換
    txt_temp = str(txt)

    if 99 < txt < 1000 :
        Hundreds_digit  = bin(int(txt_temp[0]))
        tens_digit      = bin(int(txt_temp[1]))
        ones_digit      = bin(int(txt_temp[2]))
    elif 9 < txt < 99:
        tens_digit      = bin(int(txt_temp[0]))
        ones_digit      = bin(int(txt_temp[1]))
    elif 0 < txt < 9 :
        ones_digit      = bin(int(txt_temp[0]))

    




    print (txt)

    time.sleep(loop_time-2)
