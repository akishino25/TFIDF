# -*- coding: utf-8 -*-

import mysql.connector, logging.config

#vagrant(centos)#
"""
hostname = "localhost"
user = "root"
password = "Root@123"
database = "tfidfDB"
"""

#vagrant(centos)#
hostname = "localhost"
user = "user1"
password = "user1!!"
database = "sharedb"

connection = None #mySQL DB コネクション
cur = None #mySQL DB カーソルオブジェクト

#log設定
logger = logging.getLogger()

"""
MySQL DB 接続用モジュール
"""
def dbConnect():
    global hostname, user, password, database
    global connection, cur
    connection = mysql.connector.connect(
        host = hostname,
        user = user,
        password = password,
        database = database)

    cur = connection.cursor(dictionary=True)    


"""
MySQL DB クローズ用モジュール
"""
def dbClose():
    global connection, cur
    cur.close()
    connection.close()    


"""
historyTableに存在して、tfidfTableに存在しないlinkを取得して、tfidfTableに登録する
"""
def diffInsertTable():
    logger.info("diffInsertTable is start")
    dbConnect()

    # historyTableに存在して tfidfTableに存在しないものを取得
    cur.execute("select historyTable.link from historyTable where not exists("
        "select tfidfTable.link from tfidfTable where historyTable.link = tfidfTable.link)")
    diffLinkList = cur.fetchall()
    #print(diffLinkList)

    #tfidfTableに差分登録
    for linkDic in diffLinkList:
        #%sで指定する際、引数はタプルにする必要があるらしいので、引数1つにも関わらずカッコで括って、カンマをつけている
        cur.execute("insert into tfidfTable(link) values (%s)",(linkDic["link"],))
    connection.commit()

    dbClose()    

"""
tfidfTableの全データ取得
"""
def getTfidfTable():
    dbConnect()
    cur.execute("select * from tfidfTable")
    tfTable = cur.fetchall()
    dbClose()
    return tfTable

"""
historyTableの全データ取得
"""
def getHistoryTable():
    dbConnect()
    cur.execute("select * from historyTable")
    historyTable = cur.fetchall()
    dbClose()
    return historyTable


"""
historyTableとtfidfTableを結合した結果を取得
    link, title, comment, likeflag
"""
def getMargeTable():
    dbConnect()
    cur.execute("""select tfidfTable.link, historyTable.title, historyTable.comment, tfidfTable.likeflag 
        from historyTable inner join tfidfTable 
        on historyTable.link = tfidfTable.link""")
    margeTable = cur.fetchall()
    dbClose()
    return margeTable

"""
与えられたlikeFlagのリストでtfidfTableのlikeFlag一覧を更新する
[MEMO]一旦likeFlagをすべてfalseにしてから、指定されたものだけtrueにしているが、上手い方法があるはず
"""
def setLikeFlag(likeFlagList):
    dbConnect()
    #一旦全てfalseに設定
    cur.execute("update tfidfTable set likeflag=false")
    #リストに存在するレコードはFlagをTrueにする
    for link in likeFlagList:
        cur.execute("update tfidfTable set likeflag=true where link=(%s)", (link,))
    connection.commit()
    dbClose()

"""
linkからtitleとcommentを取得
"""
def getTitleAndCommentFromLink(link):
    dbConnect()
    cur.execute("select title, comment from historyTable where link=(%s)", (link,))
    titleCommentTable = cur.fetchall()
    dbClose()
    return titleCommentTable

if __name__ == "__main__":
    #diffInsertTable()
    """
    table = getMargeTable()
    print(table)
    """