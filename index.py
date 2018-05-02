# -*- coding:utf-8 -*-

import os
from bottle import route, run, view, static_file, request
from bottle import TEMPLATE_PATH, jinja2_template as template

import mysqlOpe, tfidf

#BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#TEMPLATE_PATH.append(BASE_DIR + "/views")

"""
Topページ
"""
@route('/like') #/likeのルーティング
@view('like') #like.tplテンプレートを利用する
def like():
    #historyTable　と　tfidfTableの差分を更新する
    mysqlOpe.diffInsertTable()

    #historyTable　と tfidfTableをマージした結果を画面表示
    table = mysqlOpe.getMargeTable()
    return template("like", tables = table)

@route('/checked', method='POST')
def checked():
    #選択されたlinkを取得
    checkLikeList = request.forms.getall("likeFlag")
    print(checkLikeList)

    #選択された結果でlikeFlag更新
    mysqlOpe.setLikeFlag(checkLikeList)

    """
    TF-IDFの計算
    """

    # 全HistoryTableの{link, title+comment}　の配列を作成
    historyTable = mysqlOpe.getHistoryTable()

    #DBからselectした直後のHistoryDataのマスター
    masterHistoryTableData = []
    #linkのみの配列
    masterLinkList = []

    for record in historyTable:
        data = ""
        if(record["comment"] == None):
            data = record["title"]
        else:
            data = record["title"] + record["comment"]

        dic = {"link": record["link"], "data": data}
        masterHistoryTableData.append(dic)
        masterLinkList.append(record["link"])

    print(masterHistoryTableData)

    #dataのみ抜き出したリストを作成
    data = []
    for record in masterHistoryTableData:
        data.append(record["data"])
    print(data)

    #全HistoryTableのTFIDF計算
    outputDic = tfidf.tfidf(data)

    feature = outputDic["feature"]
    print(feature)
    print(len(feature))
    tfidfVec = outputDic["tfidfVec"]
    print(tfidfVec.toarray())

    #checkしたlinkの文書番号（配列番号）を取得
    linkNoList = []
    for link in checkLikeList:
        linkNoList.append(masterLinkList.index(link))
    print(linkNoList)

    #全HistoryTableのTFIDFベクトルから、checkしたものだけスライス
    userVec = []
    for no in linkNoList:
        userVec.append(tfidfVec[no,:])
    averageVec = tfidf.averageVecForCSCMatrix(userVec)
    print(averageVec)

    #ユーザ嗜好ベクトルの特徴語ランキング作成
    featureRanking = tfidf.rankFeature(averageVec, feature)[:50] #上位xx件でスライス
    #for data in featureRanking:
    #    print(data[0] + ":" +data[1])

    #コサイン類似度算出
    sortedCosvalueList = tfidf.rankingCosSim(averageVec, tfidfVec)
    #おすすめランキングリスト
    ranking = []
    for key, value in sortedCosvalueList:
        #print(str(key) +" : " +str(value))
        #key(文書番号)からlinkを逆引き
        link = masterLinkList[key]
        #linkからtitleとcommentを取得
        tAndC = mysqlOpe.getTitleAndCommentFromLink(link)
        title = tAndC[0]["title"]
        comment = tAndC[0]["comment"]
        #print(str(key) +" : " +link +" : " +title +" : " +comment + " : " +str(value))

        rankData = {"no":str(key), "score":str(round(value,3)), "link":link, "title":title, "comment":comment}
        ranking.append(rankData)

    return template("recommend", featureRanking = featureRanking, ranking = ranking)

@route('/css/<filename:path>') #CSSルーティング
def css(filename):
    #ルートパスを指定する
    return static_file(filename, root="/vagrant_data/css")


run(host='0.0.0.0', port=8080, debug=True)

# runが動作しなくなるので、使わないときはコメントアウトする
#if __name__ == "__main__":

