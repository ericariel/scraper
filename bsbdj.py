# -*- coding: utf-8 -*-
"""
@本程序实现对百思不得姐段子的多线程爬取

Created on Tue Apr 23 22:40:31 2019

@author: Ericariel
"""

import csv
import requests
import threading
from lxml import etree
from queue import Queue

class Producer(threading.Thread):
    def __init__(self,page_queue,txt_queue,*args,**kwargs):
        super(Producer, self).__init__(*args,**kwargs)
        self.page_queue = page_queue
        self.txt_queue = txt_queue
    def run(self):
        headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
        while True:
            if self.page_queue.empty():
                break
            url=self.page_queue.get()
            resp=requests.get(url,headers=headers)
            text=resp.text
            html=etree.HTML(text)
            txts=html.xpath('//div[@class="j-r-list-c-desc"]/a/text()')
            for txt in txts:
                self.txt_queue.put(txt)  
            print('='*30+"第%s页下载完成！"%url.split('/')[-1]+"="*30)
            
class Consumer(threading.Thread):
    def __init__(self,txt_queue,writer,gLock,*args,**kwargs):
        super(Consumer, self).__init__(*args,**kwargs)
        self.txt_queue = txt_queue
        self.writer= writer
        self.lock= gLock
    def run(self):
        while True:
            try:
                txt=self.txt_queue.get(timeout=40)
                self.lock.acquire()
                self.writer.writerow([txt])
                self.lock.release()
                print("保存一条")
            except:
                break



def main():
    page_queue=Queue(10)
    txt_queue=Queue(1000)
    gLock=threading.Lock()
    fp=open('bsbdj.csv', 'a',newline='', encoding='utf-8')
    writer = csv.writer(fp)
    base_url="http://www.budejie.com/text/{}"
    
    for x in range(1,11):
        url=base_url.format(x)
        page_queue.put(url)
    for x in range(5):
        t = Producer(page_queue,txt_queue)
        t.start()
    for x in range(5):
        t = Consumer(txt_queue,writer,gLock)
        t.start()
        
if __name__=="__main__":
    main()