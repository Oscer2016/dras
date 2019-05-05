# -*- coding=utf-8 -*-

from elasticsearch_dsl import Document, Date, Integer, Keyword, Text
from elasticsearch_dsl import Completion
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer
from elasticsearch_dsl.connections import connections

import time


connections.create_connection(hosts=['localhost'])

class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}


ik_analyzer = CustomAnalyzer('ik_max_word', filter=['lowercase'])
cur_date = time.strftime('%Y.%m.%d', time.localtime(time.time()))

class House(Document):
    title = Text(analyzer='ik_max_word', search_analyzer='ik_max_word', fields={'title': Keyword()})
    detail = Keyword()
    city = Keyword()
    #region_suggest = Completion(analyzer=ik_analyzer, search_analyzer="ik_max_word", fields={'region': Keyword()})
    region = Text(analyzer='ik_max_word', search_analyzer='ik_max_word', fields={'region': Keyword()})
    area = Keyword()
    scale = Keyword()
    floor = Keyword()
    direction = Keyword()
    price = Integer()
    picture = Keyword()
    pubdate = Keyword()
    source = Keyword()
    collection = Keyword()
    timestamp = Date()
    #tags = Text(analyzer='ik_max_word', fields={'tags':Keyword()})
    #content = Text(analyzer='ik_max_word')

    #class Meta:
    #    index = 'house'
    #    doc_type = 'spider'
    class Index:
        name = 'house_' + cur_date
        settings = {
          "number_of_shards": 1,
        }

if __name__ == '__main__':
    House.init()

