from django.db import models
from mongoengine import *
from elasticsearch_dsl import DocType, Date, Integer, Keyword, Text
from elasticsearch_dsl import Completion
from elasticsearch_dsl.analysis import CustomAnalyzer as _CustomAnalyzer
from elasticsearch_dsl.connections import connections

import time


connect('house', host='127.0.0.1', port=27017)

#class User(models.Model):
#    user_id = models.CharField(max_length=20)

class User(Document):
    username = StringField()
    password = StringField()
    collect = ListField()

    meta = {'collection': 'user'}

#for i in User.objects[:]:
#    print i.username


connections.create_connection(hosts=['localhost'])

class CustomAnalyzer(_CustomAnalyzer):
    def get_analysis_definition(self):
        return {}


ik_analyzer = CustomAnalyzer('ik_max_word', filter=['lowercase'])
cur_date = time.strftime('%Y.%m.%d', time.localtime(time.time()))

class House(DocType):
    title = Text(analyzer='ik_max_word', search_analyzer='ik_max_word', fields={'title': Keyword()})
    title_suggest = Completion(analyzer=ik_analyzer)
    detail = Keyword()
    city = Keyword()
    region = Text(analyzer='ik_max_word', search_analyzer='ik_max_word', fields={'region': Keyword()})
    region_suggest = Completion(analyzer=ik_analyzer)
    area = Integer()
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

    class Meta:
        index = 'house_' + cur_date
        doc_type = 'doc'

    class Index:
        index = 'house_' + cur_date
        doc_type = 'doc'


if __name__ == '__main__':
    House.init()

