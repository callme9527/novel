# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from items import BookDetail, BookItem

class YunqiPipeline(object):
    def __init__(self, db_url, db_name, repset_name):
        self.db_url = db_url
        self.db_name = db_name
        self.repset_name = repset_name

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_url=crawler.settings.get('DBURL'),
            db_name=crawler.settings.get('DBNAME', 'yunqi'),
            repset_name=crawler.settings.get('REPSETNAME', 'repset')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.db_url, replicaset=self.repset_name)
        self.db = self.client[self.db_name]

    def process_item(self, item, spider):
        if isinstance(item, BookItem):
            self._process_bookitem(item)
        else:
            self._process_bookdetail(item)
        return item

    def _process_bookitem(self, item):
        self.db['book'].insert(dict(item))

    def _process_bookdetail(self, item):
        new_item = {k: v.split('：'.decode('utf-8'), 1)[-1].strip() for k, v in item.items()}
        self.db.bookdetail.insert(new_item)

    def close_spider(self, spider):
        self.client.close()

