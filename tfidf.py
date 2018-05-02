# -*- coding: utf-8 -*-

import os, MeCab, numpy, sys
from scipy import sparse
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics.pairwise import cosine_similarity


"""
入力テキストをMeCabで分かち書きして、
filterで指定した品詞の単語のみ抜粋したリストを返す
[IN]text:入力テキスト
"""
def wakati(text):
    filter = "名詞" #filterで指定した単語のみ抜き出す
    wakatiList = []

    tagger = MeCab.Tagger()
    tagger.parseToNode('') #MeCabのバグ対策らしい（重要）
    node = tagger.parseToNode(text)

    while node:
        if node.feature.startswith(filter):
            wakatiList.append(node.surface)
        node = node.next

    return wakatiList


"""
文章のリストから、TFIDFのベクトルを算出する

CountVectorizerで文書毎の単語の出現回数のベクトルを作成する
TfidfTransformerで文書事の単語のTFIDFのベクトルを作成する

[OUT]outputDic.feature: 特徴ベクトルのリスト
[OUT]outputDic.tfidfVec: (行)文書 * (列)特徴語　(値)TFIDF のベクトル
"""
def tfidf(textList):

    outputDic = {}

    #---CountVectorによる単語出現回数のベクトル算出---
    """
    DF: 全文書中、その単語が出現する文書の割合
    （10文書中全てに出現するなら10/10=1.0）
    （10文書中3文書に出現するなら3/10=0.3）

    analyzer: 日本語文章を単語毎に分かち書きしたリストを返す関数
    max_df: 指定したDF以上の値を持つ単語は除外（どの文章にも出現している語は排除する）
    min_df: 指定したDF以下の値を持つ単語は除外（特定の文章にしか出現しない語は排除する）
    max_features: 上位ｘｘｘ件の語を特徴語として残す
    """
    cv = CountVectorizer(analyzer=wakati)
    #(行)文書, (列)特徴語,　(値)単語出現数 のベクトル
    count = cv.fit_transform(textList)
    #print(count.toarray()) 
    #特徴語の配列
    feature = cv.get_feature_names() #特徴語の配列


    #---TfidfTransformerによるTFIDF算出---
    """
    norm: 正規化？
    sublinear_tf: tfidf値に1を足すかどうか
    """
    tfidfTransformaer = TfidfTransformer(norm="l2", sublinear_tf=True)

    #先に算出したcountベクトルを与える
    #(行)文書 * (列)特徴語　(値)TFIDF のベクトル
    tfidf = tfidfTransformaer.fit_transform(count)
    #print(tfidf.toarray())

    outputDic["feature"] = feature
    outputDic["tfidfVec"] = tfidf

    return outputDic



"""
CSCMatrix(疎行列、1次元)のベクトルのリストから、全ベクトルの平均ベクトルを算出する
"""
def averageVecForCSCMatrix(vecList):
    #値が0のCSCMatrixを作成
    sumlist = [0] * vecList[0].shape[1] #vecListの1つ目の要素数分、0を値とするListを作成
    sumVec = sparse.lil_matrix(sumlist, dtype=numpy.float64) #listからCSCMatrixに変換

    #全てのベクトルを加算
    for vec in vecList:
        sumVec = sumVec + vec

    #ベクトル数で割って平均を算出
    li = [1/len(vecList)] * vecList[0].shape[1]
    averageVec = sumVec.multiply(li)

    return averageVec

"""
ユーザ嗜好ベクトル（averageVec）と、文書毎のTFIDFのベクトルのコサイン類似度を算出
[IN]averageVec : ユーザ嗜好ベクトル、ユーザの好みを表すベクトル
[IN]tfidfVec : 文書毎のTFIDFのベクトル集合
[OUT]sortedCosvalueList : (key:文書ID, value:コサイン類似度)　の要素の配列
"""
def rankingCosSim(averageVec, tfidfVec):
    rankDic = {}

    #avarageVec と　文書毎のVecのコサイン類似度を算出
    for docNo in range(tfidfVec.shape[0]):
        vec = tfidfVec[docNo,:] #docNo列のベクトルをスライス
        rankDic[docNo] = cosine_similarity(averageVec, vec)[0][0] #なぜか2階層ネストで値が算出されるので[0][0]で値取り出し

    #コサイン類似度でソート
    sortedCosvalueList = sorted(rankDic.items(), key=lambda x: -x[1])

    return sortedCosvalueList




if __name__ == "__main__":

    #---MeCabによる形態素解析（わかち書き）---
    data = [
        '蛙の子は蛙',
        '親の心子知らず',
        '井の中の蛙大海を知らず'
    ]

    for text in data:
        print("inputText : " +text)
        wakatiList = wakati(text)

        for word in wakatiList:
            print(word)


    #TFIDF計算
    outputDic = tfidf(data)

    feature = outputDic["feature"]
    print(feature)
    tfidfVec = outputDic["tfidfVec"]
    print(tfidfVec.toarray())

    #疎行列のベクトル平均
    vecList = [tfidfVec[0,:], tfidfVec[1,:], tfidfVec[2,:]]
    averageVec = averageVecForCSCMatrix(vecList)

    #コサイン類似度算出
    sortedCosvalueList = rankingCosSim(averageVec, tfidfVec)
    for key, value in sortedCosvalueList:
        print(str(key) +" : " +str(value))






