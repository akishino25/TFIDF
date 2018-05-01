# -*- coding: utf-8 -*-

import mysql.connector


if __name__ == "__main__":
    hostname = "localhost"
    user = "root"
    password = "Root@123"
    database = "tfidfDB"

    connection = mysql.connector.connect(
        host = hostname,
        user = user,
        password = password,
        database = database)

    cur = connection.cursor()    

    """
    # 初期データ投入
    cur.execute("insert into historyTable(link, title, comment) values (%s, %s, %s)",
     ("link001", "蛙について", "蛙の子は蛙"))
    cur.execute("insert into historyTable(link, title, comment) values (%s, %s, %s)",
     ("link002", "親について", "親の心子知らず"))
    cur.execute("insert into historyTable(link, title, comment) values (%s, %s, %s)",
     ("link003", "井戸と海について", "井の中の蛙大海を知らず"))
    connection.commit()
    """



