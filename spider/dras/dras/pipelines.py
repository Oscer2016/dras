# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from elasticsearch import Elasticsearch
from elasticsearch import helpers

from models import House

import time


class DrasElasticsearchPipeline(object):
    """
    写入数据到es中
    """
    def __init__(self):
        #self.es = Elasticsearch('localhostost:9200')
        #self.actions = []
        #self.date = time.strftime('%Y.%m.%d', time.localtime(time.time()))
        #House.init()
        pass

    def process_item(self, item, spider):
        
        #data = dict(item)
        try:
            #if len(self.actions) < 100:
            #    action = {
            #        "_index": 'house@' + self.date,
            #        "_type": item['collection'],
            #        "_source": data
            #    }
            #    self.actions.append(action)
            #else:
            #    res = helpers.bulk(self.es, self.actions)
            #    print res
            #    self.actions = []
            #self.es.index(index='house@'+self.date, doc_type=item['collection'], body=data)
            house = House()
            house.title = item['title']
            house.detail = item['detail']
            house.region = item['region']
            house.area = item['area']
            house.scale = item['scale']
            house.floor = item['floor']
            house.direction = item['direction']
            house.price = item['price']
            house.picture = item['picture']
            house.pubdate = item['pubdate']
            house.source = item['source']
            house.collection = item['collection']
            house.timestamp = item['timestamp']

            house.save()

        except Exception as e:
            print "Insert error: %s" % e

        return item

    def close_spider(self, spider):
        pass


class DrasMongodbPipeline(object):
    """
    写入数据到MongoDB中
    """
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.mdb = self.client['house']

    def process_item(self, item, spider):
        collection = self.mdb[item['collection']]
        
        data = dict(item)
        try:
            collection.insert(data)
        except Exception as e:
            print "Insert error: %s" % e

        return item

    def close_spider(self, spider):
        self.client.close()

