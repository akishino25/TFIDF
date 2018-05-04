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


# TODO
・自分用Readme拡充　※簡単なシーケンスとか

・エラーハンドリングを一切やってない

・チェック済のデータは必ず上位にくるので区別がつくようにする

・全部のランキングのほかに、最近の50件？のランキングとかも欲しい

