#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Tengwei'

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import os
from bs4 import BeautifulSoup
import requests
import traceback
import threading

headers = {                                    # 伪装请求头
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Host": "car.autohome.com.cn",
            "Referer":"http://car.autohome.com.cn/",
            "User-Agent": "Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0}"
            }

def getPicsofAuto(sourceUrl, dirName):
    """ 根据给定的url下载页面中的图片 """
    # 获得网页源码
    try:
        res = requests.get(sourceUrl, headers=headers)
        tmptext = res.text
        # with open('tmp.txt', 'r')as rd:
        #     tmptext = rd.read()
    except:
        print "获取网页源码失败"
        print traceback.format_exc()
        return False
        pass

    # if res.status_code == 200:
    if 200 == 200:
        print "正在解析网页信息...."
        soup = BeautifulSoup(tmptext, 'html.parser')

        # 解析出图片的url
        trlist = soup.find('div', attrs={"class":"uibox-con carpic-list03 border-b-solid"})
        trlist = trlist.find_all('li')
        trlist = [i.a.img['src'] for i in trlist]
        downImageViaMutiThread(trlist, dirName)

        # 解析处下一页的url(结束 if 没有下一页 else 递归继续下一页)
        nextPage = soup.find('div', attrs={"class": "pagecont"})
        nextPage = nextPage.find('a', attrs={"class": "page-item-next"})
        nextPage = nextPage['href']
        if 'pic' in nextPage:
            host = "http://car.autohome.com.cn"
            getPicsofAuto(host + nextPage, dirName)
        else:
            print "解析完毕"
            return True
    pass

def downloadPics(imgurl, dirname):
    """根据已有的图片url下载图片"""
    res = requests.get(imgurl, stream=True)
    image = res.content
    DistDir = "./" + dirname + "/"
    fileName = imgurl.split('/')[-1]
    if not os.path.exists(DistDir):
        # print "创建文件夹"
        os.makedirs(DistDir)
    print "保存图片到" + DistDir
    try:
        with open(DistDir + fileName, 'wb') as wr:
            wr.write(image)
    except:
        print "保存失败！"
        print traceback.format_exc()
        return False
    pass


def downImageViaMutiThread(urlList, dirname):
    task_threads = []  # 存储线程

    for file in urlList:
        t = threading.Thread(target=downloadPics, args=(file, dirname))
        task_threads.append(t)
    for task in task_threads:
        task.start()
    for task in task_threads:
        task.join()

if __name__ == "__main__":
     dataList = [
        # ["http://car.autohome.com.cn/pic/series/471-1-p1.html", "奥迪A4(进口)"],
        # ["http://car.autohome.com.cn/pic/series/18-1.html#pvareaid=2042220", "奥迪A6L"],
        # ["http://car.autohome.com.cn/pic/series/472-1.html#pvareaid=2042220", "奥迪A6(进口)"],
        # ["http://car.autohome.com.cn/pic/series/146-1.html#pvareaid=2042220", "奥迪A8"],
        # ["http://car.autohome.com.cn/pic/series/412-1.html#pvareaid=2042220", "奥迪Q7"],
        # ["http://car.autohome.com.cn/pic/series/65-1.html#pvareaid=2042220", "宝马5系"],
        # ["http://car.autohome.com.cn/pic/series/66-1.html#pvareaid=2042222", "宝马3系"],
        # ["http://car.autohome.com.cn/pic/series/317-1.html#pvareaid=2042220", "宝马3系(进口)"],
        # ["http://car.autohome.com.cn/pic/series/153-1.html#pvareaid=2042220", "宝马7系"],
        # ["http://car.autohome.com.cn/pic/series/270-1.html#pvareaid=2042222", "宝马6系"],
        # ["http://car.autohome.com.cn/pic/series/159-1.html#pvareaid=2042220", "宝马X5"]
         
     ]

     for i in dataList:
         getPicsofAuto(i[0], i[1])
     pass