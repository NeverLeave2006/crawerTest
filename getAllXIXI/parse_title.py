# -*- coding: utf-8 -*-
from tkinter import E
from bs4 import BeautifulSoup  # 从bs4引入BeautifulSoup

import urllib.request

import os

import MySQLdb

def insert_db(title,cls,url,cursor):
    
    # SQL 插入语句
    sql = "insert into pic_titles(title, class, url) VALUES('"+title+"','"+cls+"','"+url+"')"
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

titles={
    "yzrt":"亚洲人体",
    "omrt":"欧美人体",
    "gmsp":"国模私拍",
    "hgrt":"韩国人体",
    "rbrt":"日本人体",
    "a4u":"A4U",
    "ddrt":"大胆人体"
}

# 打开数据库连接
db = MySQLdb.connect("192.168.0.105", "root", "4004123a", "web_data", charset='utf8mb4' )

# 使用cursor()方法获取操作游标 
cursor = db.cursor()

for item in titles.keys():
    i=1
    while(True):
        file_path='getAllXIXI//'+item+'//'+titles[item]+str(i)+'.html'
        print(file_path+"==========================================================")
        if (os.path.exists(file_path)) :
            file_obj = open(file_path, 'r',encoding='gbk')  # 以读方式打开文件名为douban.html的文件
            html = file_obj.read()  # 把文件的内容全部读取出来并赋值给html变量
            file_obj.close()  # 关闭文件对象

            soup = BeautifulSoup(html, 'lxml')  # 初始化BeautifulSoup
            items = soup.find("ul",class_="ulPic")
            for a in items.find_all("a"):
                insert_db(a["title"],titles[item],'http://www.xxxrt.cc'+a["href"],cursor)  # 输出BeautifulSoup转换后的内容
                print(a["title"])
        else:
            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            break
        i+=1

# 关闭数据库连接
db.close()


