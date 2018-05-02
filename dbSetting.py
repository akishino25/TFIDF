# -*- coding: utf-8 -*-
"""
テスト用
share.htmlからデータをパースして、historyTableに書き込む
"""

import mysql.connector
from bs4 import BeautifulSoup


hostname = "localhost"
user = "root"
password = "Root@123"
database = "tfidfDB"

connection = mysql.connector.connect(
    host = hostname,
    user = user,
    password = password,
    database = database)

f = open("share.html")
html = f.read()
f.close

cur = connection.cursor(dictionary=True)    

"""
# 初期データ投入
cur.execute("insert into historyTable(link, title, comment) values (%s, %s, %s)",
 ("link001", "蛙について", "蛙の子は蛙"))
"""

# BeautifulSoupでパース
soup = BeautifulSoup(html, 'html.parser')
historyTable = soup.select("table:nth-of-type(3) > tr")
historyTable.pop(0)
for i, tr in enumerate(historyTable):
    print(i)
    tdList = tr.find_all("td")
    link = str(tdList[0].string)
    title = str(tdList[1].string)
    comment = str(tdList[2].string)

    print("link : " +link)
    print("title : " +title)
    if(comment != None) :
        print("comment : " +comment)
    print("---")

    #データごとにDB登録（INSERT）
    if(comment != None):
        cur.execute("insert into historyTable(link, title, comment) values (%s, %s, %s)",(link, title, comment))
    else:
        cur.execute("insert into historyTable(link, title) values (%s, %s)",(link, title))

    #決まった件数のみ登録
    """
    if(i > 30):
        break;
        """

connection.commit()

#　結果取得（SELECT）
"""
cur.execute("select * from historyTable")
print(cur.fetchall())
"""

"""
DBをクリア
truncate table historyTable;
"""

