# -*- coding: utf-8 -*-
"""
本程序使用多线程异步下载斗图啦网站最新表情包

Created on Tue Apr 23 07:56:18 2019

@author: Ericariel
"""

import os
import requests
from urllib import request
from lxml import etree
from queue import Queue
import threading

class Producer(threading.Thread):
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Producer,self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue
        
    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            self.parse_page(url)
      
    def parse_page(self,url):
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
            self.img_queue.put((img_url,filename))
        
class Consumer(threading.Thread):
    def __init__(self,page_queue,img_queue,*args,**kwargs):
        super(Consumer,self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue
    def run(self):
        while True:
            if  self.img_queue.empty():
                if self.page_queue.empty():
                    return
            img_url,filename = self.img_queue.get(block=True)
            request.urlretrieve(img_url,'images/'+filename)
            print(filename+'下载完成！')
    
def main():
    page_queue=Queue(10)
    img_queue=Queue(1000)
    base_url="https://www.doutula.com/photo/list/?page={}"
    #爬取1-10页最新表情包
    for x in range(1,11):
        url=base_url.format(x)
        page_queue.put(url)
        
    for x in range(5):
        t = Producer(page_queue,img_queue)
        t.start()
    for x in range(5):
        t = Consumer(page_queue,img_queue)
        t.start()
    
if __name__=="__main__":
    main()