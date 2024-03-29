# -*- coding: utf-8 -*-
import requests  
from bs4 import BeautifulSoup  # 从bs4引入BeautifulSoup    
# 2019-12-23更新，解决不能获取到响应的问题
url = "https://www.153831a86ef3.com/tupian/157053.html"  # URL不变
# 新增伪装成浏览器的header
fake_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'
}
response = requests.get(url, headers=fake_headers)  # 请求参数里面把假的请求header加上
# 保存网页到本地
file_obj = open('page.html', 'w',encoding='utf-8')  # 以写模式打开名叫 douban.html的文件
# 如果打开网页显示的是乱码那么就用下一行代码
# file_obj = open('douban.html', 'w', encoding="utf-8")  # 以写模式打开名叫 douban.html的文件，指定编码为utf-8
file_obj.write(response.content.decode('UTF-8'))  # 把响应的html内容
file_obj.close()  # 关闭文件，结束写入