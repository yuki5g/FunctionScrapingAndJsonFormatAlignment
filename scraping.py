#!C:/anaconda3/python.exe
# -*- coding: utf-8 -*-

import io
import sys
import requests
import bs4
import urllib.parse
import numpy as np
import json
import re

# 出力コーデック指定　文字化け対策
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

#定数宣言
YAHOO_AUCTION = "YAHOO_AUCTION"
AMAZON = "AMAZON"
YEN = "円"
NULL_JSON = "{}"
AMAZON_ERR_MSG1 = 'ご迷惑をおかけしています'
AMAZON_ERR_MSG2 = 'ご不便をおかけして申し訳ございません。'

# コマンドライン実行用検索ワード サンプル
# C:/anaconda3/python.exe c:/xampp/htdocs/python/scraping.py "strandberg boden7"
# 検索ワード
args = sys.argv

# args[0]はPython実行アプリケーション
# args[1]は実行ファイル
search_keyword = args[1]
# search_keyword = "strandberg boden7"

# Json形式変更用エンコクラス
# https://wtnvenga.hatenablog.com/entry/2018/05/27/113848
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.tolist()

#検索結果の件数を取得
def getTotalResult(site,ps):
    if site == YAHOO_AUCTION :
        total_result = ps.find('span', class_='Tab__subText')
        return total_result.text
    if site == AMAZON :
        total_result = ps.find_all('div',class_='a-section a-spacing-small a-spacing-top-small')
        if len(total_result) == 0:
            return NULL_JSON
        return total_result[0].text
#検索結果URL全件取得
def getAllPageUrl(site,ps):
    urls=[]

    if site == YAHOO_AUCTION :
        url = ps.find_all('a', class_='Product__titleLink')

    elif site == AMAZON :
        url = ps.find_all('a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')

    for x in url:
        if site == YAHOO_AUCTION :
            urls.append(x.attrs['href'])
        elif site == AMAZON :
            urls.append('https://www.amazon.co.jp' + x.attrs['href'])
    return urls

def formatString(value, site):
    # 商品名
    value[0] = value[0].strip().replace('\n','')

    # 値段1の加工
    value[1] = value[1].strip().replace(',','').replace('\n','')
    if site == YAHOO_AUCTION:
        value[1] = re.sub(r"[円].*",'' ,value[1]) + YEN
    elif site == AMAZON:
         value[1] = re.sub(r"[￥]",'' ,value[1]) + YEN

    # 値段2の加工
    value[2] = value[2].strip().replace(',','').replace('\n','')
    value[2] = re.sub(r"[円].*",'' ,value[2]) +YEN

    return value

def executeSearch(search_keyword,site):
    #変数宣言
    json_data = "["

    # 日本語キーワードをエンコード
    enco_keyword = urllib.parse.quote(search_keyword)
    # URLを指定
    if site == YAHOO_AUCTION :
        search_url = 'https://auctions.yahoo.co.jp/search/search?va='
    elif site == AMAZON :
        search_url = 'https://www.amazon.co.jp/s?k='

    # 検索URLに整形
    target_url = search_url + enco_keyword
    # HTML内容を取得
    url_data = requests.get(target_url)

    # 取得結果が0件の場合
    if url_data.status_code == 404 :
        print(NULL_JSON)
        return NULL_JSON

    #スクレイピング実行
    ps = bs4.BeautifulSoup(url_data.content,'html.parser')

    #検索結果の件数を取得
    # result_count = getTotalResult(site,ps)
    # print(result_count)

    #検索結果URL全件取得
    urls = getAllPageUrl(site,ps)

    count = 0
    ###個別ページ探索
    for y in urls:
        target_url2 = y
        url_data2 = requests.get(target_url2)

        #個別ページスクレイピング実行
        ps = bs4.BeautifulSoup(url_data2.content,'html.parser')

        if site == YAHOO_AUCTION :
            json_data = scrapeYahoo(ps, site, target_url2, json_data)
        elif site == AMAZON :
            json_data = scrapeAmazon(ps, site, target_url2, json_data)

        # 検索件数制限のため5件で制御
        count+=1
        if count == 5 :
            break

    # JSON形式最終処理
    # 行末の,の削除処理
    json_data = json_data[:-1]
    # 閉じカッコ付与
    json_data += "]"
    # JSONを出力
    return json_data

def scrapeYahoo(ps, site, target_url2, json_data):
    # 1.商品名
    summary1 = ps.find('h1', class_ = 'ProductTitle__text').text

    # 2.現在価格、即決価格
    #   現在価格、即決価格ともに設定されている場合、[0]=>現在価格 [1]=>即決価格
    #   現在価格のみ設定されている場合、[0]=>現在価格
    #   即決価格のみ設定されている場合、[0]=>即決価格
    summary2 = ps.find_all('dd', class_ = 'Price__value')

    # 3.即決価格
    # 即決価格、現在価格の両方が設定されている場合
    # そうでない場合は---を設定する
    if len(summary2) == 2:
        summary3 = summary2[1].text
    else:
        summary3='---'

    # 4.商品画像URL(1枚目のみ)
    summary4 = ps.find('img', alt = summary1 +'_画像1')
    # 画像が存在しない場合の処理
    summary4 = "image/noimage.jpg" if summary4 == None else summary4.get("src")

    # 5.遷移先URL
    summary5= target_url2

   # 6.取得元
    summary6 = site

    # 文字列加工
    # 商品名、価格のみ文字列を加工する
    edit_string = [summary1, summary2[0].text, summary3]
    edit_string = formatString(edit_string, site)

    # 1.商品名
    summary1 = edit_string[0]

    # 2.値段1 (現在価格)
    summary2 = edit_string[1]

    # 3.値段2(即決価格：存在する場合)
    summary3 = edit_string[2]

    # JSON配列作成処理
    json_data = createJSON(summary1, summary2, summary3, summary4, summary5, summary6, json_data)

    return json_data

def scrapeEbay(ps, site, target_url2, json_data):
    #商品名
    summary1 = ps.find('h1', class_ = 'it-ttl')
    #現在価格
    summary2 = ps.find('span', id = 'prcIsum')
    summary3='---'
    #商品画像URL(1枚目のみ)
    summary4 = ps.find('img', class_ = 'img img500 vi-img-gallery-vertical-align ')
    # 画像が存在しない場合の処理
    summary4 = "image/noimage.jpg" if summary4 == None else summary4.get("src")
    # 5.遷移先URL
    summary5= target_url2
   # 6.取得元
    summary6 = site
    # JSON配列作成処理
    json_data = createJSON(summary1, summary2, summary3, summary4, summary5, summary6, json_data)

    return json_data

def scrapeAmazon(ps, site, target_url2, json_data):
    # Amazonの処理エラーの場合
    amazon_process_error = AMAZON_ERR_MSG1 in ps.text and AMAZON_ERR_MSG2 in ps.text
    if(amazon_process_error):
        return NULL_JSON

    # Amazon Prime Videoを除外(head>titleタグ内にVideoの文字列を含む場合は除外する)
    if('Video' not in ps.find('title').text):
        #1.商品名
        summary1 = ps.find('h1', class_ = 'a-size-large a-spacing-none').text
        #2.価格
        summary2 = ps.find('span', class_ = 'a-offscreen').text
        summary3 = '---'
        #4.商品画像URL(1枚目のみ)
        summary4 = ps.find('img', id = 'landingImage')
        summary4 = "image/noimage.jpg" if summary4 == None else summary4.get("src")
        # 5.遷移先URL
        summary5= target_url2
        # 6.取得元
        summary6 = site

        # 文字列加工
        # 商品名、価格のみ文字列を加工する
        edit_string = [summary1, summary2, summary3]
        edit_string = formatString(edit_string, site)

        # 1.商品名
        summary1 = edit_string[0]

        # 2.値段1 (現在価格)
        summary2 = edit_string[1]

        # 3.値段2(即決価格：存在する場合)
        summary3 = edit_string[2]

        # JSON配列作成処理
        json_data = createJSON(summary1, summary2, summary3, summary4, summary5, summary6, json_data)
        return json_data

def createJSON(val1, val2, val3, val4, val5, val6, json_data):
    # JSON形式化処理
    label1 = "\"name\":"
    label2 = "\"price1\":"
    label3 = "\"price2\":"
    label4 = "\"image\":"
    label5 = "\"url\":"
    label6 = "\"source\":"

    # JSON配列作成
    json_data += "{" + label1 + "\"" + val1 + "\"," + label2 + "\"" + val2 + "\"," + label3 + "\"" + val3 + "\"," + label4 + "\"" + val4 + "\"," + label5 + "\"" + val5 + "\"," + label6 + "\"" + val6 + "\"" + "},"
    return json_data

#検索実行
result_yahoo = executeSearch(search_keyword,YAHOO_AUCTION)
result_amazon = executeSearch(search_keyword, AMAZON)
JoinJSON = result_yahoo + result_amazon
# JSONを整形
JoinJSON = JoinJSON.replace('][',',')
# 出力
print (JoinJSON)