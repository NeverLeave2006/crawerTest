# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup  # 从bs4引入BeautifulSoup

import urllib.request

cnt=0;
for i in range(1,34):
    # 读取文件内容到html变量里面
    file_obj = open('国模小露(舒芘)大尺度私拍高清人体_'+str(i)+'.html', 'r',encoding='gbk')  # 以读方式打开文件名为douban.html的文件
    html = file_obj.read()  # 把文件的内容全部读取出来并赋值给html变量
    file_obj.close()  # 关闭文件对象

    # /html/body/div[4]/div[2]/a[1]/img

    soup = BeautifulSoup(html, 'lxml')  # 初始化BeautifulSoup
    items = soup.find("div",class_="UsP0xCk")
    for item in items.find_all("a"):
        url=item.find("img")["src"]
        print(url)  # 输出BeautifulSoup转换后的内容
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        get_img = response.read()
        with open('国模小露(舒芘)大尺度私拍高清人体_'+str(cnt)+'.jpg', 'wb') as fb:
            fb.write(get_img)
        cnt+=1
        
