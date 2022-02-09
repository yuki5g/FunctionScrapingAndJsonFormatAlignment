# FunctionScrapingAndJsonFormatAlignment(ヤフオク・アマゾンの商品情報スクレイピング・JSONファイル受け渡し処理)

# デモ
デモ動画を録画してみたので、ご覧ください。
また、この動画で取得、表示したJsonはresult.jsonをご覧ください。
https://user-images.githubusercontent.com/42097873/153265755-67957da0-2a32-4a3c-a8f8-4a8f4271e7b2.mp4

# 特徴・機能
検索ウィンドウから引数を受け、scraping.pyへ渡します。
scraping.pyでは、アマゾン、ヤフオクから、該当する商品情報(商品名、値段、画像1枚)を抜粋し取得します。
(ソースの例では処理に時間がかかるため、検索数を上限10件に制限し処理結果を表示しています。)
また、スクレイピングした情報をJSON形式に変換し、Python→PHP→JSへ受け渡しを行う処理をしています。

# 開発環境
XAMPP 8.1.1
Python 3.9
jquery-3.6.0
PHP 8.1.1

# 注意点など
///

# 作成者
* 作成者 Y.Y.

# ライセンス
2条項BSDライセンス(https://ja.wikipedia.org/wiki/BSD%E3%83%A9%E3%82%A4%E3%82%BB%E3%83%B3%E3%82%B9)
