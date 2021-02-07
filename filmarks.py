# -*- coding: utf-8 -*-
import logging
import requests
from bs4 import BeautifulSoup as bs4
import re
import csv

# ロガーを取得する
logger = logging.getLogger(__name__)


"""
filmarksの「今話題のおすすめ映画」から
情報を取得してcsvに格納

作成日：2021年2月7日
"""

# 「今話題のおすすめ映画」url
base_url = 'https://filmarks.com/list/trend'
r = requests.get(base_url)
soup = bs4(r.text, 'lxml')

csvlist = []
csvlist.append(["上映日", "タイトル", "スコア"])  # カラム名設定

print("書き込みを開始します")

movies = soup.find_all("a", text=re.compile(">>詳しい情報を見る"))
# 上映日・タイトル・スコアをリストに格納
for movie in movies:
    next_url = 'https://filmarks.com/' + movie.get('href')
    # print(next_url)
    rr = requests.get(next_url)
    soupsoup = bs4(rr.text, 'lxml')

    show = (soupsoup.select_one(
        ".p-content-detail__other-info-title").text)[4:]  # 先頭「上映日：」の文言カット
    title = soupsoup.select_one('.p-content-detail__title span').text
    score = soupsoup.select_one('.c-rating__score').text

    csvlist.append([show, title, score])

# CSVファイルを開く。ファイルがなければ新規作成する。
f = open("今話題のおすすめ映画.csv", "w")
writecsv = csv.writer(f, lineterminator='\n')

# 出力
writecsv.writerows(csvlist)

# CSVファイルを閉じる。
f.close()

print("書き込みが完了しました")
