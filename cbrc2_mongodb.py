#!/usr/bin/env python
# -*- coding:utf-8 -*-
from gevent import monkey
monkey.patch_all()
from bs4 import BeautifulSoup
import csv,time,requests,gevent
from gevent.queue import Queue
import urllib
import json
import pymongo

#Mongodb configuration
client = pymongo.MongoClient(host='localhost', port=27017)
db = client['spider_world']
collection = db['cbrc_test']

endpage=14300#实际页数
work=Queue()
url_2='http://www.cbrc.gov.cn/search/search.jsp?page={page}'
# url_2="http://www.cbrc.gov.cn/search/search.jsp?page={page}&searchword=DOC_FORMDATE=2000.1.1%20to%202019.6.24%20AND%20DOC_TITLE=%E9%87%91%E8%9E%8D%E7%A7%9F%E8%B5%81%20&agencyShortlink="
for k in range(1,endpage+1):
    real_url=url_2.format(page=k)
    # print(real_url)
    work.put_nowait(real_url)
jzurls_info=[]
def crawler():
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
    }
    # data={
    #     "searchword": "DOC_FORMDATE=2000.1.1 to 2019.6.22",
    #     "agencycode": "",
    #     "agencyShortlink": "",
    #     "Title": "",
    #     "Relation": "AND",
    #     "Content": "",
    #     "dc1": "2000.1.1",
    #     "dc2": "2019.6.22",
    #     "sortfield": "-DOC_FORMDATE",
    #     "sub1": "检索"
    # }
    ######以下两种二选一######
    while not work.empty():
        url = work.get_nowait()
        # res = requests.post(url, headers=headers,data=data)
        res = requests.get(url, headers=headers)
        print(res.status_code,)
        bs_res = BeautifulSoup(res.text, "html.parser")
        hrefs=bs_res.find_all("a")
        print(type(hrefs))
        for href in hrefs:
            href_name = href.text
            href_url = 'http://www.cbrc.gov.cn' + href['href']
            try:
                info_type=href.parent.find_all("div")[1].contents[2]
            except IndexError:
                info_type = ""
            try:
                pulish_time = href.parent.find_all("div")[1].contents[4]
            except IndexError:
                pulish_time = ""
            # print(info_type,pulish_time)
            jzurls_info.append([href_name,href_url])
            cbrc={
                "title":href_name,
                "type":info_type,
                "pulish_time":pulish_time,
                "download_link":href_url,
            }
            result=collection.insert_one(cbrc)
            print(result)
task_list=[]
for x in range(10):#2个线程
    task=gevent.spawn(crawler)
    task_list.append(task)
gevent.joinall(task_list)
