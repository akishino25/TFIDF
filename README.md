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

# TODO

・本番機移植 -> ubuntus

・自分用Readmeを作成（後で分かるように)
　→pipで何をインストールしたかとか
　→MySQLのコマンドとか

・エラーハンドリングを一切やってない

・チェック済のデータは必ず上位にくるので区別がつくようにする

・全部のランキングのほかに、最近の50件？のランキングとかも欲しい

