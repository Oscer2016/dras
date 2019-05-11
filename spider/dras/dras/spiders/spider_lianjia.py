# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request
from dras.items import DrasItem
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

import time
import random
import requests
from lxml import etree


class SpiderLianjiaSpider(scrapy.Spider):
    name = 'spider_lianjia'
    allowed_domains = ['lianjia.com']
    start_urls = [
        'https://bj.lianjia.com/zufang/',
        'https://sh.lianjia.com/zufang/',
        'https://gz.lianjia.com/zufang/',
        'https://sz.lianjia.com/zufang/',
        'https://xa.lianjia.com/zufang/',
        'https://wh.lianjia.com/zufang/',
        'https://cs.lianjia.com/zufang/',
        'https://cq.lianjia.com/zufang/',
        'https://cd.lianjia.com/zufang/',
        'https://dl.lianjia.com/zufang/',
        'https://dg.lianjia.com/zufang/',
        'https://fs.lianjia.com/zufang/',
        'https://hz.lianjia.com/zufang/',
        'https://hf.lianjia.com/zufang/',
        'https://hui.lianjia.com/zufang/',
        'https://jn.lianjia.com/zufang/',
        'https://lf.lianjia.com/zufang/',
        'https://nj.lianjia.com/zufang/',
        'https://qd.lianjia.com/zufang/',
        'https://sjz.lianjia.com/zufang/',
        'https://sy.lianjia.com/zufang/',
        'https://su.lianjia.com/zufang/',
        'https://tj.lianjia.com/zufang/',
        'https://wx.lianjia.com/zufang/',
        'https://xm.lianjia.com/zufang/',
        'https://yt.lianjia.com/zufang/',
        'https://zh.lianjia.com/zufang/',
        'https://zs.lianjia.com/zufang/',
    ]

    def parse(self, response):
        # 构造翻页url
        for i in range(1, 101):
            purl = response.url + 'pg' + str(i)
            yield Request(url=purl, callback=self.next)

    def next(self, response):
        print response.url
        item = DrasItem()
        title = response.xpath('//p[@class="content__list--item--title twoline"]/a/text()').extract()
        detail = response.xpath('//p[@class="content__list--item--title twoline"]/a/@href').extract()
        city = response.xpath('//h1/a/text()').extract()[0][:-2]
        #region = response.xpath('//p[@class="content__list--item--des"]/a/text()').extract()
        #area = response.xpath('//p[@class="content__list--item--des"]/text()').extract()
        price = response.xpath('//span[@class="content__list--item-price"]/em/text()').extract()
        picture = response.xpath('//a[@class="content__list--item--aside"]/img/@data-src').extract()
        pubdate = response.xpath('//p[@class="content__list--item--time oneline"]/text()').extract()

        for i in range(30):
            item['title'] = title[i].strip()
            item['detail'] = response.url.split('/zufang')[0] + detail[i]
            item['city'] = city
            #item['region'] = '-'.join(region[2*i:2*i+2])
            #item['area'] = area[i*7+3].strip()

            tree = etree.HTML(requests.get(item['detail'], headers={'User-Agent':settings.get('USER_AGENT')}).text)
            district = tree.xpath('//p[@class="bread__nav__wrapper oneline"]/a[2]/text()')[0]
            town = tree.xpath('//p[@class="bread__nav__wrapper oneline"]/a[3]/text()')[0]
            item['region'] = district[:-2] + '-' + town[:-2]

            try:
                item['area'] = int(tree.xpath('//p[@class="content__article__table"]/span[3]/text()')[0][:-1])
                item['scale'] = tree.xpath('//p[@class="content__article__table"]/span[2]/text()')[0]
                item['direction'] = tree.xpath('//p[@class="content__article__table"]/span[4]/text()')[0]
                item['floor'] = tree.xpath('//ul/li[@class="fl oneline"][8]/text()')[0][3:]
            except:
                item['area'] = random.randint(30, 50)
                item['scale'] = "3室1厅1卫"
                item['direction'] = "南"
                item['floor'] = "低楼层/18层"

            item['price'] = int(price[i])
            item['picture'] = picture[i]
            item['pubdate'] = pubdate[i]
            item['source'] = '链家'
            item['collection'] = 'lianjia'
            item['timestamp'] = int(time.time()*1000)

            print item['title']
            print item['detail']
            print item['region']
            print item['area']
            print item['scale']
            print item['direction']
            print item['floor']
            print item['price']
            print item['picture']
            print item['pubdate']

            yield item

