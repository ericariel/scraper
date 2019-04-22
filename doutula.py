# -*- coding: utf-8 -*-
"""
本程序简单实现从斗图啦网站爬取并下载最新表情包

Created on Mon Apr 22 20:51:58 2019

@author: Ericariel
"""
import os
import requests
from urllib import request
from lxml import etree

def parse_page(url):
    headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
    resp=requests.get(url,headers=headers)
    text=resp.text
    html=etree.HTML(text)
    imgs=html.xpath('//div[@class="page-content text-center"]//img[@class!="gif"]')
    for img in imgs:
        img_url=img.get("data-original").rstrip("!dta")
        alt=img.get("alt")
        suffix=os.path.splitext(img_url)[1]
        filename=alt+suffix
        #对获得的图片链接进行下载保存到本地
        request.urlretrieve(img_url,'images/'+filename)
    
def main():
    base_url="https://www.doutula.com/photo/list/?page={}"
    #爬取1-10页最新表情包
    for x in range(1,11):
        url=base_url.format(x)
        parse_page(url)
        break
    
if __name__=="__main__":
    main()