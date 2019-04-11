# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 22:58:18 2019

@author: Administrator
"""

import requests
from lxml import etree

base_url='http://www.ygdy8.net'

def get_content(url):
    resp=requests.get(url)
    text=resp.content.decode(encoding='gbk', errors='ignore')
    html=etree.HTML(text)
    urls=html.xpath('//table[@class="tbspan"]//a[@class="ulink"][2]/@href')
    detail_urls= map(lambda url:base_url+url,urls)   
    return(detail_urls)
    
def get_detail(url):
    movie={}
    resp=requests.get(url)
    text=resp.content.decode(encoding='gbk', errors='ignore')
    html=etree.HTML(text)
    title=html.xpath('//div[@class="title_all"]//font/text()')[0]
    movie['title']=title
    def parse_info(info,rule):
        return info.replace(rule,"").strip()
    infos=html.xpath('//div[@id="Zoom"]//text()')
    for index,info in enumerate(infos):
        if info.startswith('◎年\u3000\u3000代'):
            info =parse_info(info,'◎年\u3000\u3000代')
            movie['years']= info
        elif info.startswith('◎产\u3000\u3000地'):
            info =parse_info(info,'◎产\u3000\u3000地')
            movie['country']= info
        elif info.startswith('◎类\u3000\u3000别'):
            info =parse_info(info,'◎类\u3000\u3000别')
            movie['category']= info            
        elif info.startswith('◎豆瓣评分'):
            info =parse_info(info,'◎豆瓣评分')
            movie['douban']= info
        elif info.startswith('◎片\u3000\u3000长'):
            info =parse_info(info,'◎片\u3000\u3000长')
            movie['duration']= info
        elif info.startswith('◎导\u3000\u3000演'):
            info =parse_info(info,'◎导\u3000\u3000演')
            movie['directors']= info
        elif info.startswith('◎主\u3000\u3000演'):
            info =parse_info(info,'◎主\u3000\u3000演')
            actors=[info]
            for i in range(index+1,100):
                actor=infos[i].strip()
                if infos[i].startswith('◎'):
                    break;
                actors.append(actor)
            movie['actors']= actors
        elif info.startswith('◎简\u3000\u3000介'):
            info =parse_info(info,'◎简\u3000\u3000介')
            profile=infos[index+1].strip()
            movie['profile']= profile
    download_url=html.xpath('//td[@bgcolor="#fdfddf"]/a/@href')[0]
    movie['download_url']= download_url   
    return(movie)
    
def spider():
    url='http://www.ygdy8.net/html/gndy/china/list_4_{}.html'
    for i in range(1,2):
        sort_url=url.format(i)
        detail_urls=get_content(sort_url)
        for detail_url in detail_urls:
            movie=get_detail(detail_url)
            print(movie)
            
if __name__=='__main__':
    spider()