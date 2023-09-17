import os
import re
import datetime
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import pandas as pd

# メインプログラム
if __name__ == '__main__':

    #既存の出力ファイル削除
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

    # URLにアクセス
    url = "https://www.amazon.co.jp/gp/bestsellers/books/492352"
    driver.get(url)

    # ブラウザのHTMLを取得
    soup = BeautifulSoup(driver.page_source, features="html.parser")

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
    soup = BeautifulSoup(driver.page_source, 'lxml')


    RankingTitleAndAuthor = soup.select("._cDEzb_p13n-sc-css-line-clamp-1_1Fn1y")
    
    # タイトル    
    RankingTitleRaw = RankingTitleAndAuthor[0::2]
    RankingTitles = []
    for title in RankingTitleRaw:
        Rankingtitle = title.get_text()
        RankingTitles.append(Rankingtitle)

    # 著作者名（できた）
    RankingAuthorRaw = RankingTitleAndAuthor[1::2]
    RankingAuthors = []
    for author in RankingAuthorRaw:
        authorName = author.get_text()
        RankingAuthors.append(authorName)


    # 販売方式（できた）
    RankingPublishRaw = soup.find_all(class_ = "a-size-small a-color-secondary a-text-normal")
    RankingPublishs = []
    for publsih in RankingPublishRaw:
        publishName = publsih.get_text()
        RankingPublishs.append(publishName)

    # 価格データの取得(できた)
    RankingPricesRaw = soup.select("._cDEzb_p13n-sc-price-animation-wrapper_3PzN2")
    RankingPrices = []
    for price in RankingPricesRaw:
        RankingPrice = int(price.get_text().replace(',', '').replace('￥',''))
        RankingPrices.append(RankingPrice)

    # レビューのデータ取得(できた)
    RankingRating = []
    RankingRateCount = []
    RankingBlock = soup.select(".zg-grid-general-faceout")
    for book in RankingBlock:
        bookrating = book.find(class_="a-icon-row")
        bookrate = 0.0
        bookrateCount = 0
        if bookrating is None: # レビュー有無チェック
            pass
        else:
            bookrate = float(bookrating.find(class_="a-icon-alt").get_text().replace('5つ星のうち', ''))
            bookrateCount = int(bookrating.find(class_="a-size-small").get_text().replace(',', ''))
        RankingRating.append(bookrate)
        RankingRateCount.append(bookrateCount)

    dt_now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    dt_now_str = str(dt_now)
    print(dt_now_str)

    # データ整理完了
    # xlsx 出力
    Ranking = list(range(1,51))

    df = pd.DataFrame({
    '順位' :Ranking,
    'タイトル' :RankingTitles,
    '著者':RankingAuthors,
    '販売方式':RankingPublishs,
    '価格':RankingPrices,
    'レビュー値':RankingRating,
    'レビュー数':RankingRateCount
    })

    excel_path = "./test.xlsx"
    df.to_excel(excel_path, sheet_name=dt_now_str, index=False, header=True, float_format="%.1f",startrow=0, startcol=0)


    """
    for book in RankingBlock:
        with open("book.txt", "a" , encoding='utf-8') as f:
            f.write(book.get_text() + "\n")
    """
