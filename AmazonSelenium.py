import os
import re
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

# メインプログラム
if __name__ == '__main__':

        #既存のコード
    if os.path.isfile("book.txt"):
        os.remove("book.txt")

    # ブラウザのオプション
    options = Options()
    options.add_argument("--blink-settings=imagesEnabled=false") # 画像の非表示
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")  # ブラウザを非表示で起動する
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    options.add_argument("--no-sandbox")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_experimental_option("useAutomationExtension", False)

    # ブラウザ起動
    service = ChromeService(executable_path="C:\chromedriver_win64\chromedriver.exe")
    driver = webdriver.Chrome(options=options)

    # 要素が見つかるまで10秒待つ
    driver.implicitly_wait(10)

    # URLにアクセス
    url = "https://www.amazon.co.jp/gp/bestsellers/books/492352"
    driver.get(url)
    time.sleep(1)

    # ブラウザのHTMLを取得
    soup = BeautifulSoup(driver.page_source, features="html.parser")

    # 要素の数をターミナルに表示
    length = len(soup.find_all(id="gridItemRoot"))
    print(f"スクロールする前のarticleの数は{length}")

    # ページの最下部へ移動する
    old_size = 0
    html_body = driver.find_element(By.XPATH, "/html/body")
    for _ in range(1, 50):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        new_size = html_body.size
        if new_size == old_size:
            print(f"{_}回スクロールしました。")
            break
        old_size = new_size

    # ブラウザのHTMLを取得
    soup = BeautifulSoup(driver.page_source, features="html.parser")

    # 要素の数をターミナルに表示
    length = len(soup.find_all(id="gridItemRoot"))
    print(f"スクロールした後のarticleの数は{length}")

    bookList = soup.find_all(id="gridItemRoot")
    for book in bookList:
        print(book.find_all(class_="a-link-normal"))
        with open("book.txt", "a" , encoding='utf-8') as f:
            f.write(book.get_text() + "\n")
