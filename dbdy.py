#!/usr/bin/env python
# coding: utf-8
#作者：Ericariel
#www.myhmt.xyz
'''
本脚本爬取电影《武林怪兽》的豆瓣短评生成词云
并通过百度NLP，对其进行情感分析，生成直方图
'''
import sys

import matplotlib.pyplot as plt
import requests
from aip import AipNlp
from bs4 import BeautifulSoup as BS
from matplotlib.font_manager import FontProperties
from wordcloud import WordCloud

class douban():
    def __init__(self):   
        APP_ID = '********'  #百度NLP的APP_ID
        API_KEY = '************************' #百度NLP的API_KEY
        SECRET_KEY = '***********************************' #SECRET_KEY
        self.client = AipNlp(APP_ID, API_KEY, SECRET_KEY)  #百度API调用
        self.lists = [] #用来存储短评的情感分数
        self.nums = 0   #计算短评总数
        self.font = FontProperties(
            fname=
            '/usr/share/fonts/adobe-source-han-serif/SourceHanSerifCN-Heavy.otf'
        ) #设置plot直方图的字体

    def get_content(self):
        print("开始爬取")
        for i in range(0, 200, 20):
            target = 'https://movie.douban.com/subject/26425062/comments?start=' + str(i) + '&limit=20&sort=new_score&status=P'
            req = requests.get(target)
            req.encoding = "UTF-8"
            html = BS(req.text)
            texts = html.find_all('span', class_='short')
            for each in texts:
                with open('yingping.txt', 'a', encoding='UTF-8') as f:
                    f.write(each.string.replace("\n", "") + '\n')
                    self.nums += 1
        print("爬取完毕，正在生成词云")

    def get_word(self):
        f = open(r'yingping.txt', 'r').read()
        wordcloud = WordCloud(
            collocations=False,
            width=2000,
            height=1860,
            margin=2,
            font_path=
            r'/usr/share/fonts/adobe-source-han-serif/SourceHanSerifCN-Heavy'
        ).generate(f)
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.show(self)
        wordcloud.to_file('result.png')
        print("词云已生成")

    def qinggan(self):
        with open('yingping.txt', 'r', encoding='UTF-8') as f:
            line = f.readline()
            i = 1
            print("正在分析情感")
            while line:
                num = self.client.sentimentClassify(
                    line.encode("gbk", 'ignore').decode(
                        "gbk", "ignore"))["items"][0]["positive_prob"]
                self.lists.append(num)
                sys.stdout.write(
                    "已分析:%.2f%%" % float(100 * (i + 1) / self.nums) + '\r')
                sys.stdout.flush()
                line = f.readline()
                i += 1
        sys.stdout.write("已下载:%.2f%%" % float(100 * (i + 1) / self.nums) +
                         '\n')
        print('分析完成')

    def get_hist(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.hist(self.lists, bins=10)
        plt.title('武林怪兽前两百条短评情感', fontproperties=self.font)
        plt.xlabel('情感积极度', fontproperties=self.font)
        plt.ylabel('数量', fontproperties=self.font)
        plt.show()


if __name__ == "__main__":
    dl = douban()
    dl.get_content()
    dl.get_word()
    dl.qinggan()
    dl.get_hist()
