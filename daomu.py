import requests,sys
from bs4 import BeautifulSoup

class downloader(object):

    def __init__(self):
        self.target = 'http://www.quanshuwang.com/book/9/9055'
        self.names = []            #存放章节名
        self.urls = []            #存放章节链接
        self.nums = 0            #章节数

    """
    函数说明:获取下载链接
    Parameters:
        无
    Returns:
        无
    """
    def get_download_url(self):
        req = requests.get(url = self.target)
        req.encoding='gb2312'
        html = req.text
        div_bf = BeautifulSoup(html,'html.parser')
        div = div_bf.find_all('div',class_="clearfix dirconone")
        a = div[0].find_all('a')
        self.nums = len(a)
        for each in a:
            self.names.append(each.string)
            self.urls.append(each.get('href'))

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
        req = requests.get(url = target)
        req.encoding='gb2312'
        html = req.text
        bf = BeautifulSoup(html,'html.parser')
        texts = bf.find_all('div',id= 'content') 
        texts = texts[0].text.replace('\xa0'*4,'').replace('style5();','').replace('style6();','')
        return texts

    """
    函数说明:将爬取的文章内容写入文件
    Parameters:
        name - 章节名称(string)
        path - 当前路径下,小说保存名称(string)
        text - 章节内容(string)
    Returns:
        无
    Modify:
        2017-09-13
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
    print('《盗墓笔记》开始下载：')
    for i in range(dl.nums):
        dl.writer(dl.names[i], '盗墓笔记.txt', dl.get_contents(dl.urls[i]))
        sys.stdout.write("  已下载:%.3f%%" %  float(i/dl.nums) + '\r')
        sys.stdout.flush()
    print('《盗墓笔记》下载完成')
