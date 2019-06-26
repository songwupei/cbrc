#!/usr/bin/env python
# -*- coding:utf-8 -*-
from gevent import monkey
monkey.patch_all()
from bs4 import BeautifulSoup
import time,requests,gevent
from gevent.queue import Queue
import pymongo

class MongodbConn(object):
    def __init__(self):
        self.CONN = pymongo.MongoClient(host='localhost', port=27017)
    def run(self):
        database = "spider_world"
        db = self.CONN[database]
        # db.authenticate("username", "password")
        # col = db.collection_names()
        col = db['cbrc_20190624']
        collection = db.get_collection(col)
        # query one document
        document = collection.find_one()
        print(document)
        # query all document
        documents = collection.find()
        for i in documents:
            # print key of (key: value)
            print(i.keys())
if __name__ == '__main__':
    mongo_obj = MongodbConn()