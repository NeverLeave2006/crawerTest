# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup  # 从bs4引入BeautifulSoup
import MySQLdb

# 打开数据库连接
db = MySQLdb.connect("192.168.1.104", "root", "4004123a", "crawler", charset='utf8' )

# 使用cursor()方法获取操作游标 
cursor = db.cursor()
cnt=0;
for i in range(1,84):
    # 读取文件内容到html变量里面
    file_obj = open('亚洲无码'+str(i)+'.html', 'r',encoding='utf-8')  # 以读方式打开文件名为douban.html的文件
    html = file_obj.read()  # 把文件的内容全部读取出来并赋值给html变量
    file_obj.close()  # 关闭文件对象

    soup = BeautifulSoup(html, 'lxml')  # 初始化BeautifulSoup
    for each_movie in soup.find_all("a", class_="tupian-pic loading"):
        print(each_movie['title'])  # 输出BeautifulSoup转换后的内容
        print(each_movie['href'])  # 输出BeautifulSoup转换后的内容pi
        cnt+=1;
        # SQL 插入语句
        sql = """insert into wm_tb values('"""+str(cnt)+"""','"""+each_movie['title']+"""','"""+each_movie['href']+"""')"""
        print(sql)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            db.commit()
            print("success")
        except:
            # Rollback in case there is any error
            db.rollback()
            print("fail")

# 关闭数据库连接
db.close()