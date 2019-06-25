#!/usr/bin/env python
# -*- coding:utf-8 -*-
from gevent import monkey
monkey.patch_all()
from bs4 import BeautifulSoup
import csv,time,requests,gevent
from gevent.queue import Queue
import urllib
import json
endpage=4#实际页数
#url_1="http://www.cbrc.gov.cn/search/search.jsp?page={page}&searchword=DOC_FORMDATE=2000.1.1%20to%202019.5.24%20AND%20DOC_TITLE={title}&agencyShortlink="
url_2='http://www.cbrc.gov.cn/search/search.jsp?page={page}'
csv_file=open("jzurl.csv","w",newline="",encoding="utf-8")
writer=csv.writer(csv_file)
work=Queue()
# for i in range(1,12):
#     for j in range(1,11):
#         real_url=url_1.format(group=i,page=j)
#         print(real_url)
#         work.put_nowait(real_url)

####以下两种网址二选一##
# for k in range(1,endpage+1):
#     real_url=url_1.format(page=k,title="金融租赁")
#     work.put_nowait(real_url)
#     print(real_url)
for k in range(1,endpage+1):
    real_url=url_2.format(page=k)
    print(real_url)
    work.put_nowait(real_url)
jzurls_info=[]
def crawler():
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
    }
    data={
        "searchword": "DOC_FORMDATE=2000.1.1 to 2019.5.24 AND DOC_TITLE=筹建 AND DOC_CLOB=金融租赁",
        "agencycode": "",
        "agencyShortlink": "",
        "Title": "筹建",
        "Relation": "AND",
        "Content": "金融租赁",
        "dc1": "2000.1.1",
        "dc2": "2019.5.24",
        "sortfield": "-DOC_FORMDATE",
        "sub1": "检索"
    }
    ######以下两种二选一######
    while not work.empty():
        url = work.get_nowait()
        res = requests.post(url, headers=headers,data=data)
        #print(res.text)
        bs_res = BeautifulSoup(res.text, "html.parser")
        hrefs=bs_res.find_all("a")
        for href in hrefs:
            href_name = href.text
            href_url = 'http://www.cbrc.gov.cn' + href['href']
            jzurls_info.append([href_name,href_url])
            print([href_name,href_url])
    print(jzurls_info)
    writer.writerows(jzurls_info)




    # while not work.empty():
    #     url=work.get_nowait()
    #     res=requests.get(url,headers=headers)
    #     print(res.status_code)
    #########以上两种方法二选一#####################################



        # bs_res=BeautifulSoup(res.json(),"html.parser")
        # group_lis=bs_res.find("div",id="sousou")#.find_all("li")
        # print(group_lis)
        # group_name=group_foods.find("h3").text[:-3]
        # print(group_name)
        # for href in group_divs[2].find("a"):
        #     href_name=href.text
        #     href_url = 'http://www.cbrc.gov.cn' + href['href']
        #     food_calorie=food.find("p").text
            # jzurls_info.append([href_name,href_url])
            # print([href_name,href_url])
    # print(jzurls_info)
    # writer.writerows(jzurls_info)
#
task_list=[]
for x in range(1):#2个线程
    task=gevent.spawn(crawler)
    task_list.append(task)
gevent.joinall(task_list)


csv_file.close()

