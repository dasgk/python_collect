# -*- coding: utf-8 -*-
import pymysql

class CsdnBlogMySql(object):
    def mysql_insert(title, author,post_time,content,look_num):
        # 打开数据库连接
        db = pymysql.connect(host="localhost",user="root",passwd="root",db="csdn",charset="utf8")
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        cursor.execute("INSERT INTO article_info(title, author, content, look_num, post_time) VALUES ('%s','%s','%s','%s','%s')" %(title,author,content,look_num,post_time))
        # 提交到数据库执行
        db.commit()
        db.close()