#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests  
from bs4 import BeautifulSoup  # 从bs4引入BeautifulSoup
import MySQLdb

# 打开数据库连接
db = MySQLdb.connect("192.168.1.104", "root", "4004123a", "crawler", charset='utf8' )

# 使用cursor()方法获取操作游标 
cursor = db.cursor()

# SQL 查询语句
sql = "SELECT * FROM wm_tb where id >='695'"
try:
   # 执行SQL语句
   cursor.execute(sql)
   # 获取所有记录列表
   results = cursor.fetchall()
   for row in results:
      id=row[0]
      name = row[1]
      href = row[2]
      # 打印结果
      print("name=%s,href=%s" % (name, href))

      # 2019-12-23更新，解决不能获取到响应的问题
      url = "https://www.b121a9be1284.com"+href  # URL不变
      # 新增伪装成浏览器的header
      fake_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'
      }
      response = requests.get(url, headers=fake_headers)  # 请求参数里面把假的请求header加上
      html=response.content.decode('UTF-8')
      soup = BeautifulSoup(html, 'lxml')  # 初始化BeautifulSoup
      link1=soup.select("#lin1k0")[0]
      static=link1["data-clipboard-text"]
      print(static)
      link2=soup.select("#lin1k1")[0]
      thunderUrl=link2["data-clipboard-text"]
      print(thunderUrl)
      
      # SQL 插入语句
      sql = """INSERT INTO wm_details_tb VALUES ('"""+id+"""', '"""+name+"""', '"""+href+"""', '"""+static+"""', '"""+thunderUrl+"""')"""
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

except:
   print("Error: unable to fecth data")

# 关闭数据库连接
db.close()