# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 22:58:18 2019

@author: ericariel
"""

import requests
from lxml import etree


movies=[]
headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
}
url="https://movie.douban.com/cinema/nowplaying/wuhan/"
resp=requests.get(url,headers=headers)

html=etree.HTML(resp.text)
ul=html.xpath('//ul[@class="lists"]')[0]

#print(etree.tostring(ul,encoding='utf-8').decode('utf-8'))

lis=ul.xpath("./li")

for li in lis:
    title=li.xpath('@data-title')[0]
    score=li.xpath('@data-score')[0]
    duration=li.xpath('@data-duration')[0]
    actors=li.xpath('@data-actors')[0]
    thumbnail=li.xpath('.//img/@src')[0]
    movie={
            'title':title,
            'score':score,
            'duration':duration,
            'actors':actors,
            'thumbnail':thumbnail}
    
    movies.append(movie)

print(movies)