# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from dras.items import DrasItem
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

import math
import json
import time
import random
import re
import requests
from lxml import etree

class Spider5i5jSpider(scrapy.Spider):
    name = 'spider_5i5j'
    allowed_domains = ['5i5j.com']
    start_urls = [
        'https://m.5i5j.com/bj/zufang',
        'https://m.5i5j.com/hz/zufang',
        'https://m.5i5j.com/sh/zufang',
        'https://m.5i5j.com/sz/zufang',
        'https://m.5i5j.com/wh/zufang',
        'https://m.5i5j.com/wx/zufang',
        'https://m.5i5j.com/cd/zufang',
        'https://m.5i5j.com/cs/zufang',
        'https://m.5i5j.com/nj/zufang',
        'https://m.5i5j.com/nn/zufang',
        'https://m.5i5j.com/tj/zufang',
        'https://m.5i5j.com/ty/zufang',
        'https://m.5i5j.com/zz/zufang',
#        'https://hz.5i5j.com/zufang',
#        'https://sh.5i5j.com/zufang',
#        'https://wh.5i5j.com/zufang'
    ]
    city_info = {
        'bj': ['北京', 29349],
        'hz': ['杭州', 13177],
        'sh': ['上海', 8552],
        'sz': ['苏州', 3839],
        'wh': ['武汉', 592],
        'wx': ['无锡', 6426],
        'cd': ['成都', 389],
        'cs': ['长沙', 939],
        'nj': ['南京', 13429],
        'nn': ['南宁', 2058],
        'tj': ['天津', 11098],
        'ty': ['太原', 7376],
        'zz': ['郑州', 287],
    }
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'cookie': '',
        'pragma': 'no-cache',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    def parse(self, response):
        # 获取当前城市房源总数
        #url = 'https://{}.5i5j.com/zufang/'.format(response.url.split('/')[3])
        #headers = {'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8', 'Accept-Encoding': 'gzip, deflate, br', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8','Upgrade-Insecure-Requests':'1', 'Host':'bj.5i5j.com','Referer':'https://bj.5i5j.com/zufang/','User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        #print requests.get(re.findall("href='(.*?)';", requests.get(url).text)[0], headers=headers).text
        #total = response.xpath('//div[@class="total-box noBor"]/span/text()').extract()
        #if total:
            #page_num = int(math.ceil(float(total[0])/30))
        #else:
            #print "获取房源总数失败!!!"

        Spider5i5jSpider.headers['referer'] = response.url + '/index'
        city = response.url.split('/')[3]
        page_num = int(math.ceil(float(Spider5i5jSpider.city_info[city][1])/30))
        
        item = DrasItem()
        # 构造翻页url
        for i in xrange(1, page_num):
            purl = response.url + '/index-n' + str(i)
            res = requests.get(purl, headers=Spider5i5jSpider.headers, allow_redirects=False).text
            try:
                houses = json.loads(res)['houses']
                for house in houses:
                    house_id = house['_source']['housesid']
                    item['title'] = house['_source']['housetitle']
                    item['detail'] = 'https://{}.5i5j.com/zufang/{}.html'.format(city, house_id)
                    item['city'] = Spider5i5jSpider.city_info[city][0]
                    try:
                        item['region'] = house['_source']['qyname'] + '-' + house['_source']['sqname'] #+ house['_source']['communityname']
                    except:
                        item['region'] = str(house['_source']['qyname']) + '-' + str(house['_source']['sqname'])
                    item['area'] = house['_source']['area']
                    item['scale'] = house['_source']['bedroom_cn'] + house['_source']['livingroom_cn'] + house['_source']['toilet_cn']
                    item['floor'] = house['_source']['floorPositionStr'] + '/' + str(house['_source']['houseallfloor'])
                    item['direction'] = house['_source']['heading']
                    item['price'] = house['_source']['price']
                    item['picture'] = house['_source']['imgurl']
                    item['pubdate'] = house['_source']['bookin_time']
                    item['source'] = '我爱我家'
                    item['collection'] = '5i5j'
                    item['timestamp'] = int(time.time()*1000)
        
                    #print house
                    print item['title']
                    print item['detail']
                    print item['city']
                    print item['region']
                    print item['area']
                    print item['scale']
                    print item['floor']
                    print item['direction']
                    print item['price']
                    print item['picture']
                    print item['pubdate']
        
                    yield item
                
                #time.sleep(random.randint(0, 10))
                time.sleep(60)
            except:
                pass
                #print res
            #yield Request(url=purl, headers=Spider5i5jSpider.headers, meta={'city_code':city,'city_name':Spider5i5jSpider.city_info[city][0]}, callback=self.next)

    def next(self, response):
        print response.url
        item = DrasItem()
        houses = json.loads(response.text)['houses']
        for house in houses:
            house_id = house['_source']['housesid']
            item['title'] = house['_source']['housetitle']
            item['detail'] = 'https://{}.5i5j.com/zufang/{}.html'.format(response.meta['city_code'], house_id)
            item['city'] = response.meta['city_name']
            try:
                item['region'] = house['_source']['qyname'] + '-' + house['_source']['sqname'] #+ house['_source']['communityname']
            except:
                item['region'] = str(house['_source']['qyname']) + '-' + str(house['_source']['sqname'])
            item['area'] = house['_source']['area']
            item['scale'] = house['_source']['bedroom_cn'] + house['_source']['livingroom_cn'] + house['_source']['toilet_cn']
            item['floor'] = house['_source']['floorPositionStr'] + '/' + str(house['_source']['houseallfloor'])
            item['direction'] = house['_source']['heading']
            item['price'] = house['_source']['price']
            item['picture'] = house['_source']['imgurl']
            item['pubdate'] = house['_source']['bookin_time']
            item['source'] = '我爱我家'
            item['collection'] = '5i5j'
            item['timestamp'] = int(time.time()*1000)

            #print house
            print item['title']
            print item['detail']
            print item['city']
            print item['region']
            print item['area']
            print item['scale']
            print item['floor']
            print item['direction']
            print item['price']
            print item['picture']
            print item['pubdate']

            yield item
        
        time.sleep(random.randint(0, 5))

