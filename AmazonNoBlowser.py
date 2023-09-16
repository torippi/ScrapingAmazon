import requests
from bs4 import BeautifulSoup
import os
import re

# beautifulSoupで要素を全て取得
def datamain():
    data = []
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15'
    header = {
        'User-Agent': user_agent
    }
    url = 'https://www.amazon.co.jp/gp/bestsellers/books/492352'
    r = requests.get(url, headers=header)
    soup = BeautifulSoup(r.content, 'lxml',from_encoding='utf-8')
    length = len(soup.select('.a-link-normal'))
    print(f"articleの数は{length}")
    elems = soup.select('.a-link-normal')
    for a in elems:
        data.append(a.text)
        value = a.get("href")
        data.append(value)
    return data


def selectdata():
    sort1 = []
    with open("link.txt", encoding='utf-8') as f:
        reader = f.readlines()
    for x in reader:
        link = re.search(r"dp/\w+", x)
        c = re.search(r"ポイント\(\d+%\)", x)
        if link is not None:
            nlink = (link.group())
            if nlink in sort1:
                pass
            if nlink not in sort1:
                nlink2 = ("https://www.amazon.co.jp/" + nlink)
                with open("sorted.txt", "a", encoding='utf-8') as f:
                    f.write(nlink2+"\n")
                sort1.append(nlink)
        elif '5つ星のうち' in x or '/product-reviews' in x:
            pass
        elif c is not None:
            pass
        else:
            with open("sorted.txt", "a", encoding='utf-8') as f:
                f.write(x)

    with open("sorted.txt", encoding='utf-8') as f:
        reader1 = f.readlines()
    for x1 in reader1:
        p = re.search(r"￥\d*,?\d*", x1)
        if len(x1) == 1:
            pass
        else:
            if p is not None:
                with open("result.txt", "a", encoding='utf-8') as f:
                    f.write(x1+"\n\n")
            else:
                with open("result.txt", "a", encoding='utf-8') as f:
                    f.write(x1)


# メインプログラム
if __name__ == '__main__':
    if os.path.isfile("result.txt"):
        os.remove("result.txt")
        os.remove("link.txt")
        os.remove("sorted.txt")

    # 
    datas = datamain()
    for d in datas:
        d = d.strip()
        with open("link.txt", "a", encoding='utf-8') as f:
            f.write(d + "\n")

    selectdata()