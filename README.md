# TFIDF

# 起動方法
./run.sh
（内部で　$nohup python3 index.py >> ./server.log &　を実行しているだけ）

# 停止方法
ps aux | grep python3
kill [プロセス番号]

# アクセス方法
http://[IPアドレス]:8080/like

#ログ関係
tfidf.log : ソースコード中に記述しているログ　（http://[IPアドレス]:8080/log　で確認できる）
server.log : 標準出力に表示されるものをパイプしているログ

#ファイル概要
・index.py : bottle起動、ルーティング
・mysqlOpe.py : MySQL操作関係
・tfidf.py : TFIDF計算関係

・views/like.tpl : 選択画面用テンプレート
・views/recommend.tpl : 推薦画面用テンプレート
・css : スタイルシート

・tfidf.conf : Vagrant　と　Ubuntuの切り替え用設定ファイル
・logging.conf : ログ設定

・server.log : 動作ログ（標準出力のリダイレクト）
・tfidf.log : ロガーによる動作ログ（整形されているもの）

・run.sh : 起動用シェル

・dbSetting.py : テストDB構築用スクリプト（Vagrant用）　本番環境では利用しない
・share.html : テストDB構築時のshareMoviewDownloadのページサンプル　本番環境では利用しない


# Ubuntu移植
## python, pipインストール
$sudo add-apt-repository ppa:deadsnakes/ppa
$sudo apt-get update
$sudo apt-get install python3.6 python3.6-dev
$mkdir -p $HOME/bin
$ln -s /usr/bin/python3.6 $HOME/bin/python
$sudo vi .bash_profile
---
export PATH=$HOME/bin:$PATH
---
## pipモジュールインストール
$sudo python3 -m pip install --upgrade pip
$sudo pip3 install numpy scipy scikit-learn
## mecab関係インストール
$sudo apt-get install mecab libmecab-dev mecab-ipadic mecab-ipadic-utf8
$sudo pip3 install mecab-python3
## bottle関係インストール
$sudo pip3 install bottle==0.12.12
$sudo pip3 install jinja2
## mysql関係インストール　　※centOSとUbuntuでインストールするものが異なるので注意
$sudo apt-get install python3-mysql.connector
## mysqlにTable作成
$mysql -u root -p
>>use sharedb;
>>create table tfidfTable(link varchar(20), likeflag tinyint(1))
+----------+-------------+------+-----+---------+-------+
| Field    | Type        | Null | Key | Default | Extra |
+----------+-------------+------+-----+---------+-------+
| link     | varchar(20) | YES  |     | NULL    |       |
| likeflag | tinyint(1)  | YES  |     | NULL    |       |
+----------+-------------+------+-----+---------+-------+

#処理概要
◎/likeアクセス時
　・historyTableはshareMovieDownloadのプログラムで日々更新されるので、
　　アクセス時にhistoryTableの更新分をtfidfTableに反映する

　・ブラウザ上にtfidfTableのlink,likeFlag　と historyTableのtitle,commentを
　　マージして表示する

◎/checkedアクセス時
　・/likeでチェックした内容で、tfidfTableのlikeFlagを全て書き換える
　　（TODO：全件更新する必要はないので差分だけ更新するよう改善の余地あり）

　・今後計算のためのマスターデータを作っておく
　　　・masterHistoryTableData : {link, data} を要素にもつ配列
　　　　※data: title + commentの文字列
　　　・masterLinkList : linkを要素にもつ配列
　　　※それぞれ配列の順番はhistoryTableの上位(旧)→下位(新)となっている

　・data(title+comment)を抜き出したリストを作成し、
　　それをもとに全historyTableのTFIDFベクトルを作成
　　　・feature : 特徴語の配列
　　　・tfidfVec : (行)文書 * (列)特徴語　(値)TFIDF のベクトル

　・/likeでチェックした文書番号を取得して、
　　tfidfVecからその文書番号の行を抽出（スライス）
　　　・userVec : (行)文書 * (列)特徴語　(値)TFIDF のベクトル
　　　　※行はチェックした文書のみ

　・userVecの全行を列ごとに合計して、行数で平均を取ることで、
　　1次元のユーザ嗜好ベクトルを作成
　　　・averageVec : (行)1行のみ * (列)特徴語　(値)TFIDF平均 のベクトル

　・userVecの値でソートして、ユーザが好みの特徴語をランキング

　・解析対象（最新ｘｘ件）の選択に応じて、tfidfVecを下(新)から切り取り
　　・selectTfidfVec : (行)文書 * (列)特徴語　(値)TFIDF のベクトル
　　　※行は下からｘｘ件で切り出し

　・selectTfidfVecの各行　と　averageVec でコサイン類似度を算出
　　・sourtedCosvalueList : (key:文書番号, value:コサイン類似度)　の要素の配列
　　　※コサイン類似度でソート済

　・ソート結果にlink,title,commentを加えて画面表示

# TODO
・エラーハンドリングを一切やってない

・チェック済のデータは必ず上位にくるので区別がつくようにする

