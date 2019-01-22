#!/usr/bin/env python
# coding: utf-8
# 作者：Ericariel
# www.myhmt.xyz
import sys
import requests
from bs4 import BeautifulSoup

class downloader(object):

    def __init__(self):
        self.target="https://www.w3cschool.cn/articlelist/all?page="
        self.server="https://www.w3cschool.cn"
        self.names = []           #存放标题
        self.urls = []            #存放链接
        self.times = []           #新闻时间
        self.nums = 0             #总新闻数目

    """
    函数说明:获取下载链接
    Parameters:
        无
    Returns:
        无
    """
    def get_download_url(self):
        for i in range(2):
            req=requests.get(self.target+str(i))
            html=req.text
            text=BS(html)
            texts=text.find_all('div',class_='news-list')
            get_list=texts[0].find_all('h4')
            for each in get_list:
                if each.b.string=="[w3c开发者日报]":
                    self.names.append(each.a.get("title"))
                    self.urls.append(self.server+each.a.get('href'))
                    self.times.append(each.span.string)
        self.nums = len(self.names)

    """
    函数说明:获取章节内容
    Parameters:
        target - 下载连接(string)
    Returns:
        texts - 章节内容(string)
    Modify:
        2019-01-21
    """
    def get_contents(self, target):
        req=requests.get(target)
        html=req.text.replace('<p>','\n').replace('<h2>','\n').replace('<h3>','\n')
        text=BS(html)
        texts=text.find_all('div',class_='article-page-content content-intro')
        return texts[0].text

    """
    函数说明:将爬取的文章内容写入文件
    Parameters:
        name - 新闻名称(string)
        path - 当前路径下,新闻保存名称(string)
        text - 新闻内容(string)
    Returns:
        无
    Modify:
        2019-01-22
    """
    def writer(self, name, path, text):
        write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(text)
            f.write('\n\n')

if __name__ == "__main__":
    dl = downloader()
    dl.get_download_url()
    print('每日简讯开始下载：')
    for i in range(dl.nums):
        dl.writer(dl.names[i], '每日简讯.txt', dl.times[i]+dl.get_contents(dl.urls[i]))
        sys.stdout.write("已下载:%.2f%%" %  float(100*(i+1)/dl.nums) + '\r')
        sys.stdout.flush()
    sys.stdout.write("已下载:%.2f%%" %  float(100*(i+1)/dl.nums) + '\n')
    print('每日简讯下载完成')




