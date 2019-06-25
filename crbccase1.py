#!/usr/bin/env python
# -*- coding:utf-8 -*-
#!/usr/bin/env python
# -*- coding:utf-8 -*-
##链接地址##http://www.cbrc.gov.cn/search/index.jsp##
##银监会查询文件##
# from gevent import monkey
# monkey.patch_all()
# import gevent,requests,bs4,csv
# from gevent.queue import Queue
#
# work = Queue()
#
# url_1 = 'http://www.cbrc.gov.cn/search/index.jsp'
# work.put_nowait(url_1)
#
# url_2 = 'http://www.mtime.com/top/tv/top100/index-{page}.html'
# for x in range(1,11):
#     real_url = url_2.format(page=x)
#     work.put_nowait(real_url)
#
# def crawler():
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
#     while not work.empty():
#         url = work.get_nowait()
#         res = requests.get(url,headers=headers)
#         bs_res = bs4.BeautifulSoup(res.text,'html.parser')
#         datas = bs_res.find_all('div',class_="mov_con")
#         for data in datas:
#             TV_title = data.find('a').text
#             data = data.find_all('p')
#             TV_data =''
#             for i in data:
#                 TV_data =TV_data + ''+ i.text
#             writer.writerow([TV_title,TV_data])
#             print([TV_title,TV_data])
#
# csv_file = open('timetop.csv','w',newline='',encoding='utf-8')
# writer = csv.writer(csv_file)
#
# task_list = []
# for x in range(3):
#     task = gevent.spawn(crawler)
#     task_list.append(task)
# gevent.joinall(task_list)
#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
import pyautogui


#URL = 'https://y.qq.com/n/yqq/song/000xdZuV2LcQ19.html'
SEQUENCE = 'CCTAAACTATAGAAGGACAGCTCAAACACAAAGTTACCTAAACTATAGAAGGACAGCTCAAACACAAAGTTACCTAAACTATAGAAGGACAGCTCAAACACAAAGTTACCTAAACTATAGAAGGACAGCTCAAACACAAAGTTACCTAAACTATAGAAGGACA' #'GAGAAGAGAAGAGAAGAGAAGAGAAGAGAAGAGAAGAGAAGAGAAGAGAAGAGAAGAGAAGAGAAGAGAAGAGAAGAGAAGAGAAGAGAAGAGAAGAGAAGAGAAGAGAAGAGAAGAGAAGAGAAGAGAAGA'
# 用selenium打开网页
# (首先要下载 Chrome webdriver, 或 firefox webdriver)
driver = webdriver.Chrome()
URL="http://www.cbrc.gov.cn/search/index.jsp"
driver.get(URL)
time.sleep(2)
title=driver.find_element_by_name("Title")
title.send_keys("金融租赁")
# assistant=driver.find_element_by_id("assistant")
# assistant.send_keys("宋失")
# time.sleep(2)
button=driver.find_element_by_name("sub1")
button.click()
#
time.sleep(2)
#

hrefs=driver.find_elements_by_partial_link_text("股权")
print(hrefs)
for href in hrefs:
    href_add = href.get_attribute('href')
    print(href_add+href.text)
# for link in driver.find_elements_by_xpath("//*[@href]"):#获取当前页面的href
#     print link.get_attribute('href')
href_nextpage=driver.find_element_by_link_text("下一页")
nextpage=href_nextpage.get_attribute("href")
print(nextpage)
href_endpage=driver.find_element_by_link_text("尾页")
endpage=href_endpage.get_attribute("href")[46:48]
print(endpage)
time.sleep(2)
driver.close()


