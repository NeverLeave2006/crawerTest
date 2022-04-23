# -*- coding: utf-8 -*-
from urllib.error import HTTPError
from bs4 import BeautifulSoup  # 从bs4引入BeautifulSoup

import requests 

import MySQLdb

# 设置状态
def set_status(url,cursor):
    # SQL 修改语句
    sql = "update pic_titles set state=1 where url='"+url+"'"
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()

def insert_all(url,imgs,cursor):
    print(imgs)
    try:
        for i in imgs:
            # SQL 修改语句
            sql = "insert into web_data.imgs(url, pic) values('"+url+"','"+i+"')"
            # 执行sql语句
            cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
    
        

def parse_content(content):
    pics=[]
    soup = BeautifulSoup(content, 'lxml')  # 初始化BeautifulSoup
    # "/html/body/div[3]/div[2]/a[1]"

    imgs=soup.select("body > div > div > a > img ")
    for img in imgs:
        pics.append(img["src"])
        # print(img["src"])
    return pics

#处理url
def deal_url(url,cursor):
    url_=url.replace(".html","")
    idx=1
    imgs=[]
    while(True):
        if idx==1:
            target = url_+".html"  # URL不变
        else:
            target = url_+"_"+str(idx)+".html"  # URL不变
        # 新增伪装成浏览器的header
        fake_headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3947.100 Safari/537.36'
        }
        # 捕获异常
        try:
            # 设置超时为3秒
            response = requests.get(target, headers=fake_headers,timeout=3)  # 请求参数里面把假的请求header加上
            #结果
            content=response.content.decode('gbk')
            # with open('getAllXIXI//page//tp'+str(idx)+'.html', 'w') as f:
            #     f.write(content)
            print(target)
            pics=parse_content(content)
            imgs.extend(pics)
            idx+=1
        # 超时异常
        except requests.ReadTimeout:
            print('timeout')
            continue
            # HTTP异常
        # 请求异常
        except requests.RequestException:
            print('reqerror')
            continue
        except HTTPError:
            print('httperror')
            break
        except UnicodeDecodeError:
            print('UnicodeDecodeError')
            break
        
    print("==========================================================")

    # # 归纳数组
    insert_all(url,imgs,cursor)
    
    # # 设置状态
    set_status(url,cursor)


# 打开数据库连接
db = MySQLdb.connect("192.168.0.105", "root", "4004123a", "web_data", charset='utf8mb4' )

# 使用cursor()方法获取操作游标 
cursor = db.cursor()

# SQL 查询语句
sql = "SELECT distinct url FROM pic_titles where state=0"
try:
    # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    for row in results:
        url = row[0]
        # 打印结果
        deal_url(url,cursor)
except:
    print("Error: unable to fetch data")

# 关闭数据库连接
db.close()
